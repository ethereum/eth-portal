from eth.chains import (
    MainnetChain,
)
from eth.rlp.headers import (
    BlockHeader,
)
from eth.rlp.logs import (
    Log,
)
from eth.rlp.receipts import (
    Receipt,
)
from eth.vm.forks.london.blocks import (
    LondonBlockHeader,
)
from eth_utils import (
    to_bytes,
    to_canonical_address,
    to_int,
)
from eth_utils.toolz import (
    assoc,
)


def block_fields_to_header(web3_block_fields):
    """
    Convert a web3 block into an rlp-serializable object.

    A web3 block is the result of a w3.eth.getBlock() request. An
    rlp-serializable object is one that can be passed in as an argument to
    rlp.encode(). Hashing that result must always return the hash of the block.
    """
    header_fields = _select_header_fields(web3_block_fields)
    if 'base_fee_per_gas' in header_fields:
        return LondonBlockHeader(**header_fields)
    else:
        return BlockHeader(**header_fields)


def _select_header_fields(block_fields):
    """
    Select and format the fields needed to create an RLP Serializable object.

    Inspired by py-evm's eth/tools/fixtures/helpers.py
    """
    base_fields = {
        'parent_hash': block_fields['parentHash'],
        'uncles_hash': block_fields['sha3Uncles'],
        'coinbase': to_bytes(hexstr=block_fields['miner']),
        'state_root': block_fields['stateRoot'],
        'transaction_root': block_fields['transactionsRoot'],
        'receipt_root': block_fields['receiptsRoot'],
        'bloom': to_int(block_fields['logsBloom']),
        'difficulty': block_fields['difficulty'],
        'block_number': block_fields['number'],
        'gas_limit': block_fields['gasLimit'],
        'gas_used': block_fields['gasUsed'],
        'timestamp': block_fields['timestamp'],
        'extra_data': block_fields['extraData'],
        'mix_hash': block_fields['mixHash'],
        'nonce': block_fields['nonce'],
    }

    if 'baseFeePerGas' in block_fields:
        return assoc(base_fields, 'base_fee_per_gas', block_fields['baseFeePerGas'])
    else:
        return base_fields


def receipt_fields_to_receipt(web3_receipt_fields, block_number):
    """
    Convert a web3 receipt into an rlp-serializable object.
    """
    # Get appropriate Virtual Machine rules for given block number
    VM = MainnetChain.get_vm_class_for_block_number(block_number)
    ReceiptBuilder = VM.block_class.receipt_builder

    if 'type' not in web3_receipt_fields or web3_receipt_fields.type == "0x0":
        return _build_legacy_receipt(web3_receipt_fields)
    else:
        # TODO remove to_int() when web3py starts normalizing internally
        type_int = to_int(hexstr=web3_receipt_fields.type)
        legacy = _build_legacy_receipt(web3_receipt_fields)
        return ReceiptBuilder.typed_receipt_class(type_int, legacy)


def _build_legacy_receipt(fields):
    built_logs = [
        Log(
            address=to_canonical_address(web3_log.address),
            topics=list(map(to_int, web3_log.topics)),
            data=to_bytes(hexstr=web3_log.data),
        )
        for web3_log in fields.logs
    ]

    # See eth/vm/forks/byzantium/constants.py for state root encodings
    # Field used to be the state root, but is now just a binary status indicator
    if fields.status == 0:
        state_root = b''
    elif fields.status == 1:
        state_root = b'\x01'
    else:
        state_root = fields.status.to_bytes(32, 'big')

    return Receipt(
        state_root=state_root,
        gas_used=fields.cumulativeGasUsed,
        logs=built_logs,
    )
