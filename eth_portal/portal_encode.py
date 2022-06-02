import ssz

from .ssz_sedes import (
    BLOCK_BODY_SEDES,
    BLOCK_KEY_SEDES,
    BLOCK_RECEIPTS_SEDES,
    BODY_TYPE_BYTE,
    HEADER_TYPE_BYTE,
    RECEIPT_TYPE_BYTE,
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


def block_body_content_value(transactions, encoded_uncles):
    """
    Compile a list of transactions and uncle headers into a block body content value.

    The uncles are already combined in a list and rlp-encoded, so they are just
    a byte-string.
    """
    # Awkward quirk that ssz must take an iterable of individual bytes, instead of `bytes`
    encoded_transactions = [
        [bytes([byte]) for byte in transaction.encode()] for transaction in transactions
    ]
    encoded_uncles = [bytes([byte]) for byte in encoded_uncles]
    return ssz.encode((encoded_transactions, encoded_uncles), BLOCK_BODY_SEDES)


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
