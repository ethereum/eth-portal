import pytest

from eth_portal.web3_encoding import (
    header_content_id,
)


@pytest.mark.parametrize(
    'chain_id, header_hash, expected_encoding',
    (
        (2, b'H' * 32, b'\x01\x02\x00' + b'H' * 32),
    )
)
def test_encode_header(chain_id, header_hash, expected_encoding):
    content_id = header_content_id(header_hash, chain_id)
    assert content_id == expected_encoding
