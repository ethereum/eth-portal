#!/usr/bin/env python3

"""
Generate private keys and their associated Portal Network Node IDs.

This is useful for grinding to find node IDs near a certain value.

For example, to generate a bunch of node IDs, then find the one closest to 0:
```
./scripts/make_node_ids.py 100000 >>all_node_ids
grep "^00" node_ids | sort | head -1
```

In the above example, one could sort without the grep and still be correct. We
demonstrate with grep for two reasons:

1. It's useful when you want to find an ID close to something other than 0.
2. Even when looking for 0, it speeds things up noticeably, by avoiding sorting
    the whole list.
"""

import secrets

from eth_keys.datatypes import (
    PrivateKey,
)
from eth_utils import (
    keccak,
)


def make_ids(num_nodes):
    for _ in range(num_nodes):
        private_key = secrets.token_bytes(32)
        public_key = PrivateKey(private_key).public_key.to_bytes()
        node_id = keccak(public_key)
        print(node_id.hex(), private_key.hex())


if __name__ == "__main__":
    import sys

    args = sys.argv
    if len(args) != 2:
        sys.exit("Must supply the number of node IDs you wish to generate")
    else:
        num_nodes = int(args[-1])
        make_ids(num_nodes)
