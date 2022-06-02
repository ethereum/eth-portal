from contextlib import ExitStack, contextmanager
import os
import sys
import time
from typing import Iterable

from eth_utils import decode_hex

from eth_portal.bridge.handle import handle_new_header
from eth_portal.bridge.insert import PortalInserter
from eth_portal.trin import launch_trin

INVALID_KEY_ENV_ERROR = (
    "Must supply environment variable PORTAL_BRIDGE_KEYS, as a"
    " comma-separated list of hex-encoded Portal client 32-byte private keys"
)


def header_log_loop(w3, portal_inserter, event_filter, poll_interval):
    while True:
        for header_hash in event_filter.get_new_entries():
            handle_new_header(w3, portal_inserter, header_hash)
        time.sleep(poll_interval)


def launch_bridge():
    # Launch trin nodes, for broadcasting data
    # The context manager shuts down all trin nodes on context exit
    trin_node_keys = load_private_keys()
    with launch_trin_inserters(trin_node_keys) as portal_inserter:
        # Monitor for new headers on mainnet
        from web3.auto.infura import w3

        block_filter = w3.eth.filter("latest")

        # On each new header, publish the content to the trin nodes
        header_log_loop(w3, portal_inserter, block_filter, 6)


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
