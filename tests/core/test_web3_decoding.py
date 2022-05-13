from eth_hash.auto import (
    keccak,
)
import rlp

from eth_portal.web3_decoding import (
    header_fields_to_header,
)


def test_web3_header_to_rlp(web3_header):
    header = header_fields_to_header(web3_header)
    header_rlp = rlp.encode(header)
    assert keccak(header_rlp) == web3_header.hash
