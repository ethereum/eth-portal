#!/usr/bin/env python3
import time

from eth_portal.bridge import (
    handle_new_header,
    launch_trin_inserters,
)


def header_log_loop(w3, portal_inserter, event_filter, poll_interval):
    while True:
        for header_hash in event_filter.get_new_entries():
            handle_new_header(w3, portal_inserter, header_hash)
        time.sleep(poll_interval)


def launch_bridge():
    #TODO Load private keys for launching trin nodes from environment
    trin_node_keys = [
        b'rainbowsunicornsrainbowsunicorns',
    ]

    # Launch trin nodes, for broadcasting data
    # The context manager shuts down all trin nodes on context exit
    with launch_trin_inserters(trin_node_keys) as portal_inserter:
        # Monitor for new headers on mainnet
        from web3.auto.infura import w3
        block_filter = w3.eth.filter('latest')

        # On each new header, publish the content to the trin nodes
        header_log_loop(w3, portal_inserter, block_filter, 6)


if __name__ == '__main__':
    try:
        launch_bridge()
    except KeyboardInterrupt:
        print("Clean exit of bridge launcher")
