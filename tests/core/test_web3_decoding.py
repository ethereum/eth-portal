from eth.db.trie import (
    _make_trie_root_and_nodes,
)
from eth_hash.auto import (
    keccak,
)
from hexbytes import (
    HexBytes,
)
import rlp

from eth_portal.web3_decoding import (
    block_fields_to_header,
    receipt_fields_to_receipt,
)


def test_web3_header_to_rlp(web3_block):
    header = block_fields_to_header(web3_block)
    assert header.hash == web3_block.hash
    header_rlp = rlp.encode(header)
    assert keccak(header_rlp) == web3_block.hash


def test_receipt_root_from_fields(block_info_and_web3_receipts):
    (block_number, receipt_root), web3_receipts = block_info_and_web3_receipts
    receipts = [
        receipt_fields_to_receipt(web3_receipt, block_number)
        for web3_receipt in web3_receipts
    ]
    assert all(receipts)

    # check fields:
    for idx, (receipt, web3_receipt) in enumerate(zip(receipts, web3_receipts)):
        # blooms equal
        generated_bloom = HexBytes(receipt.bloom.to_bytes(256, 'big'))
        assert generated_bloom == web3_receipt.logsBloom

        # status/state-root equal
        if receipt.state_root == b'':
            assert web3_receipt.status == 0
        elif receipt.state_root == b'\x01':
            assert web3_receipt.status == 1
        else:
            assert HexBytes(web3_receipt.status) == receipt.state_root

        # type equal
        if receipt.type_id is None:
            assert web3_receipt.type == "0x0"
        else:
            assert hex(receipt.type_id) == web3_receipt.type

        # cumulative gas used
        assert receipt.gas_used == web3_receipt.cumulativeGasUsed

    # Compare to receipt root
    calculated_root, _ = _make_trie_root_and_nodes(tuple(receipt.encode() for receipt in receipts))

    assert calculated_root == receipt_root
