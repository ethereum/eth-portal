#!/usr/bin/env python3
import os
import sys
import time

from eth_utils import decode_hex

from eth_portal.bridge import (
    handle_new_header,
    launch_trin_inserters,
)


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
        block_filter = w3.eth.filter('latest')

        # On each new header, publish the content to the trin nodes
        header_log_loop(w3, portal_inserter, block_filter, 6)


def load_private_keys():
    try:
        concat_keys = os.environ['PORTAL_BRIDGE_KEYS']
    except KeyError:
        sys.exit(INVALID_KEY_ENV_ERROR)
    else:
        hex_keys = concat_keys.split(',')
        keys = [decode_hex(key) for key in hex_keys]
        if any(len(key) != 32 for key in keys):
            sys.exit(INVALID_KEY_ENV_ERROR)
        else:
            return keys


if __name__ == '__main__':
    try:
        launch_bridge()
    except KeyboardInterrupt:
        print("Clean exit of bridge launcher")
