import ssz
from ssz.sedes import (
    Container,
    Vector,
    uint8,
    uint16,
)

#
# SSZ encoding
#

HEADER_TYPE_BYTE = b'\x00'
RECEIPT_TYPE_BYTE = b'\x02'
BLOCK_KEY_SEDES = Container((
    uint16,  # Chain ID
    Vector(uint8, 32),  # header hash
))


def header_content_key(header_hash, chain_id=1):
    """
    Convert a header hash into a header content key for the Portal History Network.

    Include the chain ID, which defaults to mainnet.
    """
    # The header type ID is implicitly defined in the SSZ union which
    # specifies the content key on the header history network.
    encoded = ssz.encode((chain_id, header_hash), BLOCK_KEY_SEDES)

    # I don't think py-ssz supports Union types, so manually tacking it on
    return HEADER_TYPE_BYTE + encoded


def receipt_content_key(header_hash, chain_id=1):
    """
    Convert a header hash into a receipt content key for the Portal History Network.

    Include the chain ID, which defaults to mainnet.
    """
    # See implementation notes in header_content_key()
    encoded = ssz.encode((chain_id, header_hash), BLOCK_KEY_SEDES)
    return RECEIPT_TYPE_BYTE + encoded
