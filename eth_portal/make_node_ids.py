#!/usr/bin/env python3

"""
Generate passwords and their associated Portal Network Node IDs

Generate a bunch of node IDs, then find the one closest to 0
```
./eth_portal/make_node_ids.py 100000 >>all_node_ids
grep "^00" node_ids | sort | head -1
```

grep isn't strictly necessary, above. It's useful when you want to find an ID
close to something other than 0. Even when looking for 0, it speeds things up a
bit, by avoiding sorting the whole list.
"""

import secrets

from eth_keys.datatypes import PrivateKey
from eth_utils import keccak


def make_ids(num_nodes):
    for _ in range(num_nodes):
        private_key = secrets.token_bytes(32)
        public_key = PrivateKey(private_key).public_key.to_bytes()
        node_id = keccak(public_key)
        print(node_id.hex(), private_key.hex())

if __name__ == '__main__':
    import sys
    args = sys.argv
    if len(args) != 2:
        sys.exit("Must supply the number of node IDs you wish to generate")
    else:
        num_nodes = int(args[-1])
        make_ids(num_nodes)
