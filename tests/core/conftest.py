import pytest


@pytest.fixture
def web3_header():
    with open('tests/full_block.example') as f:
        # These classes are used by the repr of the block, so ignore F401
        from web3.datastructures import AttributeDict  # noqa: F401
        from hexbytes import HexBytes  # noqa: F401

        return eval(f.read())
