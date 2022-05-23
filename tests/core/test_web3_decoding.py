from eth_hash.auto import (
    keccak,
)
import rlp

from eth_portal.web3_decoding import (
    block_fields_to_header,
)


def test_web3_header_to_rlp(web3_block):
    header = block_fields_to_header(web3_block)
    assert header.hash == web3_block.hash
    header_rlp = rlp.encode(header)
    assert keccak(header_rlp) == web3_block.hash
