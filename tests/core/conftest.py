from hexbytes import HexBytes  # noqa: F401; HexBytes used by eval()
import pytest
from web3.datastructures import (  # noqa: F401; AttributeDict used by eval()
    AttributeDict,
)

HEADER_FILES = [
    "tests/full_block.example",
    "tests/full_block_with_uncle.example",
]


def _eval_from_file(filename):
    with open(filename) as f:
        return [eval(line.strip()) for line in f.readlines()]


def _eval_one_from_file(filename):
    items = _eval_from_file(filename)
    return items[0]


@pytest.fixture(params=HEADER_FILES)
def web3_block(request):
    return _eval_one_from_file(request.param)


@pytest.fixture
def web3_block_and_receipts():
    web3_block = _eval_one_from_file("tests/full_block_with_uncle.example")
    receipts = _eval_from_file("tests/receipts_block14764013.example")
    return (
        web3_block,
        receipts,
    )
