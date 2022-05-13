#!/usr/bin/env python3

from web3.auto.infura import w3
import time

def handle_new_header_hash(header_hash):
    print(header_hash)
    block = w3.eth.getBlock(header_hash, full_transactions=True)
    print(repr(block))

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_new_header_hash(event)
        time.sleep(poll_interval)

def main():
    block_filter = w3.eth.filter('latest')
    log_loop(block_filter, 6)

if __name__ == '__main__':
    main()
