from eth.rlp.headers import BlockHeader
from eth.vm.forks.london.blocks import LondonBlockHeader
from eth_utils import to_bytes, to_int
from eth_utils.toolz import assoc
import rlp


def _select_header_fields(header_fields):
    # also, select only the fields relevant to creating a header.
    # cribbed from py-evm's eth/tools/fixtures/helpers.py
    base_fields = {
        'parent_hash': header_fields['parentHash'],
        # TODO calculate hash from list of uncles 'uncles_hash': header_fields['uncleHash'],
        'coinbase': to_bytes(hexstr=header_fields['miner']),
        'state_root': header_fields['stateRoot'],
        'transaction_root': header_fields['transactionsRoot'],
        'receipt_root': header_fields['receiptsRoot'],
        'bloom': to_int(header_fields['logsBloom']),
        'difficulty': header_fields['difficulty'],
        'block_number': header_fields['number'],
        'gas_limit': header_fields['gasLimit'],
        'gas_used': header_fields['gasUsed'],
        'timestamp': header_fields['timestamp'],
        'extra_data': header_fields['extraData'],
        'mix_hash': header_fields['mixHash'],
        'nonce': header_fields['nonce'],
    }
    if 'baseFeePerGas' in header_fields:
        return assoc(base_fields, 'base_fee_per_gas', header_fields['baseFeePerGas'])
    else:
        return base_fields


def header_fields_to_rlp(web3_header_fields):
    header_fields = _select_header_fields(web3_header_fields)
    if 'base_fee_per_gas' in header_fields:
        header = LondonBlockHeader(**header_fields)
    else:
        header = BlockHeader(**header_fields)
    return rlp.encode(header)
