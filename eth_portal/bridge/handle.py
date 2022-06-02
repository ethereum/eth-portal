from eth_portal.web3_decode import web3_result_to_transaction

from .history import propagate_block_bodies, propagate_header, propagate_receipts
from .insert import PortalInserter


def handle_new_header(
    w3, portal_inserter: PortalInserter, header_hash: bytes, chain_id=1
):
    """
    Handle header hash notifications by posting all new data to Portal History Network.

    This data to be propagated will at least include header, block bodies
    (uncles & transactions), and receipts. At documentation time, only headers
    are propagated.

    :param w3: web3 access to core Ethereum content
    :param portal_inserter: a class responsible for pushing content keys and
        values into the network via a group of running portal clients
    :param header_hash: the new header hash that we were notified exists on the network
    :param chain_id: Ethereum network Chain ID that this header exists on
    """
    block_fields = propagate_header(w3, portal_inserter, chain_id, header_hash)

    # Convert web3 transactions to py-evm transactions
    transactions = [
        web3_result_to_transaction(web3_transaction, block_fields.number)
        for web3_transaction in block_fields.transactions
    ]

    propagate_block_bodies(w3, portal_inserter, chain_id, block_fields, transactions)
    propagate_receipts(w3, portal_inserter, chain_id, block_fields, transactions)
