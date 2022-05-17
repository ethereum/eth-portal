from eth_hash.auto import (
    keccak,
)
from eth_utils import (
    ValidationError,
    encode_hex,
)
import rlp

from eth_portal.web3_decoding import (
    header_fields_to_header,
)
from eth_portal.web3_encoding import (
    header_content_id,
)


def handle_new_header(w3, portal_inserters, header_hash, chain_id=1):
    propagate_header(w3, portal_inserters, header_hash, chain_id)
    # TODO propagate bodies & receipts


def propagate_header(w3, portal_inserters, header_hash, chain_id):
    """
    React to new header hash notification by posting header to Portal History Network.

    :param w3: web3 access to get core Ethereum content
    :param portal_inserters: a class responsible for pushing content IDs and
        values into the network
    :param header_hash: the new header hash that we were notified exists on the network
    :param chain_id: which Chain ID does this header exist on?
    """
    # Retrieve data to post to network
    block_fields = w3.eth.getBlock(header_hash, full_transactions=False)
    if block_fields.uncles:
        block_fields.uncleHeaders = [
            w3.eth.getBlock(uncle_hash) for uncle_hash in block_fields.uncles
        ]

    # Encode data for posting
    content_id, content_value = header_fields_to_content(block_fields, chain_id)

    # Post data to trin nodes
    portal_inserters.push(content_id, content_value)


def header_fields_to_content(header_fields, chain_id):
    header = header_fields_to_header(header_fields)
    header_rlp = rlp.encode(header)

    if keccak(header_rlp) != header_fields.hash:
        raise ValidationError(
            f"Could not correctly encode header fields {header_fields} to {header!r}"
        )

    content_id = header_content_id(header_fields.hash, chain_id)
    return content_id, header_rlp


class PortalInserters:
    def push(self, content_id, content_value):
        # TODO actually push data to connected trin nodes
        print(
            "Propagate new content with ID, value:",
            encode_hex(content_id),
            ",",
            encode_hex(content_value),
        )
