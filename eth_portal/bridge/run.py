from contextlib import ExitStack, contextmanager
import logging
import os
import sys
import time
from typing import Iterable

from eth_utils import decode_hex
from web3 import Web3

from eth_portal.bridge.handle import handle_new_header, propagate_block
from eth_portal.bridge.inject import inject_content
from eth_portal.bridge.insert import PortalInserter
from eth_portal.trin import launch_trin

INVALID_KEY_ENV_ERROR = (
    "Must supply environment variable PORTAL_BRIDGE_KEYS, as a"
    " comma-separated list of hex-encoded Portal client 32-byte private keys"
)

INVALID_CLOUDFLARE_AUTH_PROVIDER_ENV_ERROR = (
    "Must supply the following environment variables to use an authenticated"
    "cloudflare provider: \nAUTH_CLIENT_ID, AUTH_CLIENT_SECRET, AUTH_CLIENT_URL"
)


class DroppedFilter(Exception):
    pass


def header_log_loop(w3, portal_inserter, event_filter, poll_interval):
    while True:
        try:
            new_entries = event_filter.get_new_entries()
        except ValueError as exc:
            # most likely: the filter was dropped by the node
            logging.exception("Failure to get latest events, re-attempting...")
            raise DroppedFilter from exc

        for header_hash in new_entries:
            handle_new_header(w3, portal_inserter, header_hash)
        time.sleep(poll_interval)


def poll_chain_head(portal_inserter, w3):
    """
    Monitor the head of the chain, and insert new content until Ctrl-C is pressed.
    """
    while True:
        block_filter = w3.eth.filter("latest")

        try:
            # On each new header, publish the content to the trin nodes
            header_log_loop(w3, portal_inserter, block_filter, 6)
        except DroppedFilter:
            print("Recreating filter to watch for latest headers")
            continue


def backfill_bridge_blocks(portal_inserter, start_block, end_block, w3):
    block_numbers = range(start_block, end_block + 1)
    print(f"Injecting {len(block_numbers)} blocks, starting from #{start_block}")

    for block_num in block_numbers:
        print(f"Getting block #{block_num} for injection to Portal network")
        block_fields = w3.eth.get_block(block_num, full_transactions=True)
        print(f"Injecting block hash {block_fields.hash.hex()}")
        propagate_block(w3, portal_inserter, block_fields)

    print("Finished injecting all blocks")


def launch_bridge(provider_arg):
    # Launch trin nodes, for broadcasting data
    # The context manager shuts down all trin nodes on context exit
    trin_node_keys = load_private_keys()
    w3 = load_provider(provider_arg)
    with launch_trin_inserters(trin_node_keys) as portal_inserter:
        poll_chain_head(portal_inserter, w3)


def launch_injector(content_files):
    trin_node_keys = load_private_keys()
    with launch_trin_inserters(trin_node_keys) as portal_inserter:
        inject_content(portal_inserter, content_files)


def launch_backfill(start_block, end_block, provider_arg):
    trin_node_keys = load_private_keys()
    w3 = load_provider(provider_arg)
    with launch_trin_inserters(trin_node_keys) as portal_inserter:
        backfill_bridge_blocks(portal_inserter, start_block, end_block, w3)


def launch_patch_recent(blocks_to_patch, provider_arg):
    trin_node_keys = load_private_keys()
    w3 = load_provider(provider_arg)
    end_block = w3.eth.get_block("latest").get("number")
    if blocks_to_patch > end_block:
        start_block = 0
    else:
        start_block = end_block - blocks_to_patch
    with launch_trin_inserters(trin_node_keys) as portal_inserter:
        backfill_bridge_blocks(portal_inserter, start_block, end_block, w3)


@contextmanager
def launch_trin_inserters(keys: Iterable[bytes]):
    """
    For each key supplied, launch an instance of trin, then yield an object for propagation.

    When this context manager exits, all the trin instances will also exit.

    Yields a :class:`PortalInserter` instance, to push data to the whole group
    of launched trin nodes.

    :param keys: list of private keys to launch each trin instance.
    """
    with ExitStack() as stack:
        web3_links = [
            stack.enter_context(launch_trin(key, 9000 + idx))
            for idx, key in enumerate(keys)
        ]
        yield PortalInserter(web3_links)


def load_private_keys():
    try:
        concat_keys = os.environ["PORTAL_BRIDGE_KEYS"]
    except KeyError:
        sys.exit(INVALID_KEY_ENV_ERROR)
    else:
        hex_keys = concat_keys.split(",")
        keys = [decode_hex(key) for key in hex_keys]
        if any(len(key) != 32 for key in keys):
            sys.exit(INVALID_KEY_ENV_ERROR)
        else:
            return keys


def load_provider(provider_arg):
    if provider_arg == "cloudflare-auth":
        try:
            client_id = os.environ["AUTH_CLIENT_ID"]
            client_secret = os.environ["AUTH_CLIENT_SECRET"]
            client_url = os.environ["AUTH_CLIENT_URL"]
        except KeyError:
            sys.exit(INVALID_CLOUDFLARE_AUTH_PROVIDER_ENV_ERROR)
        headers = {
            "headers": {
                "Content-Type": "application/json",
                "CF-Access-Client-Id": client_id,
                "CF-Access-Client-Secret": client_secret,
            }
        }
        w3 = Web3(Web3.HTTPProvider(client_url, request_kwargs=headers))
        if not w3.isConnected():
            raise RuntimeError(
                "Invalid authenticated cloudflare provider credentials, provider is not connected."
            )
        return w3
    else:
        from web3.auto.infura import w3

        return w3
