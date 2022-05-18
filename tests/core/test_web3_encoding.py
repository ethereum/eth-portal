from eth_utils import (
    decode_hex,
)
import pytest

from eth_portal.web3_encoding import (
    header_content_key,
)


@pytest.mark.parametrize(
    'chain_id, header_hash, expected_encoding',
    (
        (2, b'H' * 32, b'\x00\x02\x00' + b'H' * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/2fb0116314c407feff4ce678dac2da5adea834eb/content-keys-test-vectors.md#headerkey
            15,
            decode_hex('0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d'),
            decode_hex('0x000f00d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d'),
        ),
    )
)
def test_encode_header(chain_id, header_hash, expected_encoding):
    content_key = header_content_key(header_hash, chain_id)
    assert content_key == expected_encoding
