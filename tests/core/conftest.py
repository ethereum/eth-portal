from hexbytes import HexBytes
import pytest
from web3.datastructures import (  # noqa: F401; AttributeDict used by eval()
    AttributeDict,
)

HEADER_FILES = [
    "tests/full_block.example",
    "tests/full_block_with_uncle.example",
]


@pytest.fixture(params=HEADER_FILES)
def web3_block(request):
    with open(request.param) as f:
        return eval(f.read())


@pytest.fixture
def block_info_and_web3_receipts():
    with open("tests/receipts_block14764013.example") as f:
        return (
            (
                # block number
                14764013,
                # header hash
                HexBytes(
                    "0x720704f3aa11c53cf344ea069db95cecb81ad7453c8f276b2a1062979611f09c"
                ),
                # receipt root
                HexBytes(
                    "0x168a3827607627e781941dc777737fc4b6beb69a8b139240b881992b35b854ea"
                ),
            ),
            # web3 receipt objects
            [eval(line.strip()) for line in f.readlines()],
        )
