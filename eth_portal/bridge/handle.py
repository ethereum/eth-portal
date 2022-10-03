from .history import propagate_block
from .insert import PortalInserter


def handle_new_header(w3, portal_inserter: PortalInserter, header_hash: bytes):
    """
    Handle header hash notifications by posting all new data to Portal History Network.

    This data to be propagated will at least include header, block bodies
    (uncles & transactions), and receipts. At documentation time, only headers
    are propagated.

    :param w3: web3 access to core Ethereum content
    :param portal_inserter: a class responsible for pushing content keys and
        values into the network via a group of running portal clients
    :param header_hash: the new header hash that we were notified exists on the network
    """
    # Retrieve data to post to network
    block_fields = w3.eth.get_block(header_hash, full_transactions=True)

    propagate_block(w3, portal_inserter, block_fields)
