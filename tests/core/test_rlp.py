from eth_hash.auto import keccak

from eth_portal.rlp import header_fields_to_rlp


def test_web3_header_to_rlp(web3_header):
    header_rlp = header_fields_to_rlp(web3_header)
    assert keccak(header_rlp) == web3_header.hash
