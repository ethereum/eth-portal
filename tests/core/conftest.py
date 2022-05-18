import pytest

HEADER_FILES = [
    'tests/full_block.example',
    'tests/full_block_with_uncle.example',
]


@pytest.fixture(params=HEADER_FILES)
def web3_block(request):
    with open(request.param) as f:
        # These classes are used by the repr of the block, so ignore F401
        from web3.datastructures import AttributeDict  # noqa: F401
        from hexbytes import HexBytes  # noqa: F401

        return eval(f.read())
