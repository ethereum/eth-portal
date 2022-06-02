from typing import Tuple

from eth.db.trie import make_trie_root_and_nodes
from eth_hash.auto import keccak
from eth_utils import ValidationError
import rlp

from eth_portal.portal_encode import (
    block_body_content_key,
    block_body_content_value,
    header_content_key,
    receipt_content_key,
    receipt_content_value,
)
from eth_portal.web3_decode import (
    block_fields_to_header,
    receipt_fields_to_receipt,
    web3_result_to_transaction,
)

from .insert import PortalInserter


def propagate_header(
    w3, portal_inserter: PortalInserter, chain_id: int, header_hash: bytes
):
    """
    React to new header hash notification by posting header to Portal History Network.

    :param w3: web3 access to core Ethereum content
    :param portal_inserter: a class responsible for pushing content keys and
        values into the network via a group of running portal clients
    :param chain_id: Ethereum network Chain ID that this header exists on
    :param header_hash: the new header hash that we were notified exists on the network

    :return: the web3 block fields for the given header hash
    """
    # Retrieve data to post to network
    block_fields = w3.eth.get_block(header_hash, full_transactions=True)

    # Encode data for posting
    content_key, content_value = block_fields_to_content(block_fields, chain_id)

    # Post data to trin nodes
    portal_inserter.push_history(content_key, content_value)

    return block_fields


def block_fields_to_content(block_fields, chain_id) -> Tuple[bytes, bytes]:
    """
    Convert a web3 block into a Portal History Network content key and value.

    A web3 block is the result of a w3.eth.get_block() request. A content key and
    value are the byte-strings specified by the Portal Network Spec.

    :return: (content_key, content_value)

    :raise ValidationError: if the rlp-encoded header does not match the header
        hash in `block_fields`
    """
    header = block_fields_to_header(block_fields)
    header_rlp = rlp.encode(header)

    if keccak(header_rlp) != block_fields.hash:
        raise ValidationError(
            f"Could not correctly encode header fields {block_fields} to {header!r}"
        )

    if header.hash != block_fields.hash:
        raise ValidationError(
            "py-evm generated a different hash than we did manually with"
            f" header fields {block_fields} to {header!r}"
        )

    content_key = header_content_key(block_fields.hash, chain_id)
    return content_key, header_rlp


def propagate_block_bodies(
    w3, portal_inserter: PortalInserter, chain_id: int, block_fields, transactions
):
    """
    Post block bodies to the Portal History Network.

    :param w3: web3 access to core Ethereum content
    :param portal_inserter: a class responsible for pushing content keys and
        values into the network via a group of running portal clients
    :param chain_id: Ethereum network Chain ID that this header exists on
    :param block_fields: the web3 block fields for the header to retrieve
        transactions and uncles from
    """
    # Retrieve data to post to network
    web3_uncles = [w3.eth.get_block(uncle) for uncle in block_fields.uncles]

    # Encode data for posting
    content_key, content_value = _encode_block_body_content(
        transactions,
        web3_uncles,
        chain_id,
        block_fields.hash,
        block_fields.number,
        block_fields.transactionsRoot,
        block_fields.sha3Uncles,
    )

    # Post data to trin nodes
    portal_inserter.push_history(content_key, content_value)


def encode_block_body_content(
    web3_transactions,
    web3_uncles,
    chain_id: int,
    header_hash: bytes,
    block_number: int,
    transactions_root: hash,
    uncles_root: hash,
) -> Tuple[bytes, bytes]:
    """
    Generate a Portal History Network content key and value for a block body.

    A block body is made up of the transaction bodies and the headers for the uncles.

    :return: (content_key, content_value)

    :raise ValidationError: if the encoded transactions or uncles do not match the
        header's `transactions_root` or `uncles_root` respectively
    """
    # Convert web3 transactions to py-evm transactions
    transactions = [
        web3_result_to_transaction(web3_transaction, block_number)
        for web3_transaction in web3_transactions
    ]

    return _encode_block_body_content(
        transactions,
        web3_uncles,
        chain_id,
        header_hash,
        block_number,
        transactions_root,
        uncles_root,
    )


def _encode_block_body_content(
    transactions,
    web3_uncles,
    chain_id: int,
    header_hash: bytes,
    block_number: int,
    transactions_root: hash,
    uncles_root: hash,
) -> Tuple[bytes, bytes]:
    # Just like encode_block_body_content, but the transactions are already
    # decoded from web3

    # Validate against the transactions root
    calculated_transaction_root, _ = make_trie_root_and_nodes(transactions)
    if calculated_transaction_root != transactions_root:
        raise ValidationError(
            f"Could not correctly encode transactions for header {header_hash.hex()}"
        )

    # Convert web3 (uncle) headers into py-evm headers
    uncles = [block_fields_to_header(web3_header) for web3_header in web3_uncles]
    encoded_uncles = rlp.encode(uncles)

    # Validate against the uncles root
    calculated_uncle_root = keccak(encoded_uncles)
    if calculated_uncle_root != uncles_root:
        raise ValidationError(
            f"Could not correctly encode uncles for header {header_hash.hex()}"
        )

    content_key = block_body_content_key(header_hash, chain_id)
    content_value = block_body_content_value(transactions, encoded_uncles)
    return content_key, content_value


def propagate_receipts(
    w3, portal_inserter: PortalInserter, chain_id: int, block_fields, transactions
):
    """
    React to new header hash notification by posting receipts to Portal History Network.

    :param w3: web3 access to core Ethereum content
    :param portal_inserter: a class responsible for pushing content keys and
        values into the network via a group of running portal clients
    :param chain_id: Ethereum network Chain ID that this header exists on
    :param block_fields: the web3 block fields for the header to retrieve receipts from
    """
    # Retrieve data to post to network
    txn_hashes = [keccak(txn.encode()) for txn in transactions]

    print("Collecting receipts to propagate...")
    web3_receipts = [
        w3.eth.wait_for_transaction_receipt(txn_hash, poll_latency=2)
        for txn_hash in txn_hashes
    ]
    print("Collected receipts")

    # Encode data for posting
    content_key, content_value = encode_receipts_content(
        web3_receipts,
        chain_id,
        block_fields.hash,
        block_fields.number,
        block_fields.receiptsRoot,
    )

    # Post data to trin nodes
    portal_inserter.push_history(content_key, content_value)


def encode_receipts_content(
    web3_receipts,
    chain_id: int,
    header_hash: bytes,
    block_number: int,
    receipt_root: hash,
) -> Tuple[bytes, bytes]:
    """
    Generate a Portal History Network content key and value, from a list of web3 receipts.

    :return: (content_key, content_value)

    :raise ValidationError: if the encoded receipts do not match the header's `receipt_root`
    """
    # Convert web3 receipts to py-evm receipts
    receipts = [
        receipt_fields_to_receipt(receipt, block_number) for receipt in web3_receipts
    ]

    # Validate against the receipt root
    calculated_root, _ = make_trie_root_and_nodes(receipts)
    if calculated_root != receipt_root:
        raise ValidationError(
            f"Could not correctly encode receipts for header {header_hash.hex()}"
        )

    content_key = receipt_content_key(header_hash, chain_id)
    content_value = receipt_content_value(receipts)
    return content_key, content_value
