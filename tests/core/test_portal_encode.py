from eth_utils import decode_hex
import pytest

from eth_portal.portal_encode import (
    block_body_content_key,
    header_content_key,
    receipt_content_key,
)


@pytest.mark.parametrize(
    "header_hash, expected_encoding",
    (
        (b"H" * 32, b"\x00" + b"H" * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/2fb0116314c407feff4ce678dac2da5adea834eb/content-keys-test-vectors.md#headerkey
            decode_hex(
                "0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
            decode_hex(
                "0x00d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
        ),
    ),
)
def test_encode_header_key(header_hash, expected_encoding):
    content_key = header_content_key(header_hash)
    assert content_key == expected_encoding


@pytest.mark.parametrize(
    "header_hash, expected_encoding",
    (
        (b"H" * 32, b"\x01" + b"H" * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/b75886b1b4287291d1967974a97f914d91618167/content-keys-test-vectors.md#bodykey
            decode_hex(
                "0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
            decode_hex(
                "0x01d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
        ),
    ),
)
def test_encode_block_body_key(header_hash, expected_encoding):
    content_key = block_body_content_key(header_hash)
    assert content_key == expected_encoding


@pytest.mark.parametrize(
    "header_hash, expected_encoding",
    (
        (b"H" * 32, b"\x02" + b"H" * 32),
        (
            # Pulled test data from:
            # https://github.com/ethereum/portal-network-specs/blob/2fb0116314c407feff4ce678dac2da5adea834eb/content-keys-test-vectors.md#receiptskey
            decode_hex(
                "0xd1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
            decode_hex(
                "0x02d1c390624d3bd4e409a61a858e5dcc5517729a9170d014a6c96530d64dd8621d"
            ),
        ),
    ),
)
def test_encode_receipt_key(header_hash, expected_encoding):
    content_key = receipt_content_key(header_hash)
    assert content_key == expected_encoding
