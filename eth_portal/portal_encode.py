import ssz
from ssz.sedes import Byte, Container, List, Vector, uint8, uint16

#
# SSZ encoding
#

# Blocks:
HEADER_TYPE_BYTE = b"\x00"
BODY_TYPE_BYTE = b"\x01"
RECEIPT_TYPE_BYTE = b"\x02"
BLOCK_KEY_SEDES = Container(
    (
        uint16,  # Chain ID
        Vector(uint8, 32),  # header hash
    )
)

BLOCK_RECEIPTS_SEDES = List(
    # Each encoded receipt
    List(Byte(), 65535),  # TODO identify true upper-bound on encoded receipt length
    65535,  # 2**16-1 receipts would use up >1.3 billion gas at 21k gas each
)


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


def block_body_content_key(header_hash, chain_id=1):
    """
    Convert a header hash into a block body content key for the Portal History Network.

    Include the chain ID, which defaults to mainnet.
    """
    # See implementation notes in header_content_key()
    encoded = ssz.encode((chain_id, header_hash), BLOCK_KEY_SEDES)
    return BODY_TYPE_BYTE + encoded


def receipt_content_key(header_hash, chain_id=1):
    """
    Convert a header hash into a receipt content key for the Portal History Network.

    Include the chain ID, which defaults to mainnet.
    """
    # See implementation notes in header_content_key()
    encoded = ssz.encode((chain_id, header_hash), BLOCK_KEY_SEDES)
    return RECEIPT_TYPE_BYTE + encoded


def receipt_content_value(receipts) -> bytes:
    """
    Compile a list of encoded receipts into their joined content value.
    """
    # Awkward quirk that ssz must take an iterable of individual bytes, instead of `bytes`
    quirky_byte_list = [
        [bytes([byte]) for byte in receipt.encode()] for receipt in receipts
    ]
    return ssz.encode(quirky_byte_list, BLOCK_RECEIPTS_SEDES)
