from eth_utils import decode_hex
import pytest

from eth_portal.portal_encode import (
    block_body_content_key,
    header_content_key,
    receipt_content_key,
)


@pytest.mark.parametrize(
    "chain_id, header_hash, expected_encoding",
    (
        (2, b"H" * 32, b"\x00\x02\x00" + b"H" * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/2fb0116314c407feff4ce678dac2da5adea834eb/content-keys-test-vectors.md#headerkey
            15,
            decode_hex(
                "0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
            decode_hex(
                "0x000f00d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
        ),
    ),
)
def test_encode_header_key(chain_id, header_hash, expected_encoding):
    content_key = header_content_key(header_hash, chain_id)
    assert content_key == expected_encoding


@pytest.mark.parametrize(
    "chain_id, header_hash, expected_encoding",
    (
        (2, b"H" * 32, b"\x01\x02\x00" + b"H" * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/b75886b1b4287291d1967974a97f914d91618167/content-keys-test-vectors.md#bodykey
            20,
            decode_hex(
                "0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
            decode_hex(
                "0x011400d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
        ),
    ),
)
def test_encode_block_body_key(chain_id, header_hash, expected_encoding):
    content_key = block_body_content_key(header_hash, chain_id)
    assert content_key == expected_encoding


@pytest.mark.parametrize(
    "chain_id, header_hash, expected_encoding",
    (
        (2, b"H" * 32, b"\x02\x02\x00" + b"H" * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/2fb0116314c407feff4ce678dac2da5adea834eb/content-keys-test-vectors.md#receiptskey
            4,
            decode_hex(
                "0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
            decode_hex(
                "0x020400d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
        ),
    ),
)
def test_encode_receipt_key(chain_id, header_hash, expected_encoding):
    content_key = receipt_content_key(header_hash, chain_id)
    assert content_key == expected_encoding
