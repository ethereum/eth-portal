import ssz

from .ssz_sedes import (
    BLOCK_BODY_SEDES,
    BLOCK_KEY_SEDES,
    BLOCK_RECEIPTS_SEDES,
    BODY_TYPE_BYTE,
    HEADER_TYPE_BYTE,
    RECEIPT_TYPE_BYTE,
)


def header_content_key(header_hash):
    """
    Convert a header hash into a header content key for the Portal History Network.
    """
    # The header type ID is implicitly defined in the SSZ union which
    # specifies the content key on the header history network.
    encoded = ssz.encode((header_hash,), BLOCK_KEY_SEDES)

    # I don't think py-ssz supports Union types, so manually tacking it on
    return HEADER_TYPE_BYTE + encoded


def block_body_content_key(header_hash):
    """
    Convert a header hash into a block body content key for the Portal History Network.
    """
    # See implementation notes in header_content_key()
    encoded = ssz.encode((header_hash,), BLOCK_KEY_SEDES)
    return BODY_TYPE_BYTE + encoded


def block_body_content_value(transactions, encoded_uncles):
    """
    Compile a list of transactions and uncle headers into a block body content value.

    The uncles are already combined in a list and rlp-encoded, so they are just
    a byte-string.
    """
    encoded_transactions = [transaction.encode() for transaction in transactions]
    return ssz.encode((encoded_transactions, encoded_uncles), BLOCK_BODY_SEDES)


def receipt_content_key(header_hash):
    """
    Convert a header hash into a receipt content key for the Portal History Network.
    """
    # See implementation notes in header_content_key()
    encoded = ssz.encode((header_hash,), BLOCK_KEY_SEDES)
    return RECEIPT_TYPE_BYTE + encoded


def receipt_content_value(receipts) -> bytes:
    """
    Compile a list of encoded receipts into their joined content value.
    """
    encoded_receipts = [receipt.encode() for receipt in receipts]
    return ssz.encode(encoded_receipts, BLOCK_RECEIPTS_SEDES)
