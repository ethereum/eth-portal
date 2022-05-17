#!/usr/bin/env python3
import time

from eth_portal.bridge import (
    PortalInserters,
    handle_new_header,
)


def header_log_loop(w3, event_filter, poll_interval):
    portal_inserters = PortalInserters()

    while True:
        for header_hash in event_filter.get_new_entries():
            handle_new_header(w3, portal_inserters, header_hash)
        time.sleep(poll_interval)


def launch_bridge():
    from web3.auto.infura import w3
    block_filter = w3.eth.filter('latest')
    header_log_loop(w3, block_filter, 6)


if __name__ == '__main__':
    launch_bridge()
