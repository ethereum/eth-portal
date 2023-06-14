from eth_utils import (
    ValidationError,
    keccak,
)
from eth_utils.toolz import (
    assoc,
)
from hexbytes import (
    HexBytes,
)
import pytest
from web3.datastructures import (
    AttributeDict,
)

from eth_portal.bridge.history import (
    block_fields_to_content,
    encode_block_body_content,
    encode_receipts_content,
)

EXPECTED_CONTENT_BY_HASH = {
    HexBytes("0xe137900645bb727b8cd3d2bca2e1af46a9270fb59feb08969668a322583f8af7"): (
        b"\x00\xe17\x90\x06E\xbbr{\x8c\xd3\xd2\xbc\xa2\xe1\xafF\xa9'\x0f\xb5\x9f\xeb\x08\x96\x96h\xa3\"X?\x8a\xf7",  # noqa: E501
        (
            b"\xf9\x02\x13\xa0\x81\x0fH\xed\x10\xc5}j>\xcd\xf5D\xd7\n\xbe\xcbb\xae0\xbd"
            b"\xe2\xe8m>\xa6\x10g\xb18w\xa6Q\xa0\x1d\xccM\xe8\xde\xc7]z\xab\x85\xb5"
            b"g\xb6\xcc\xd4\x1a\xd3\x12E\x1b\x94\x8at\x13\xf0\xa1B\xfd@\xd4\x93G\x94\xeag"
            b"O\xdd\xe7\x14\xfd\x97\x9d\xe3\xed\xf0\xf5j\xa9qk\x89\x8e\xc8\xa0\x8f"
            b"\xfa\xef\rj)}N*,\xab\xa0\xb1\xf2\xb9\x06\xd7\x1d=\xf9Y<W\x1c\x94\x0eto0"
            b"\xcc\xcd\xce\xa02\xfd\xad\xc7q\xe6sjVn\xac\x96'\x7f-T\xe0\xd6\xc8\x19"
            b"_\xc8)\xb3\x82\x82\xfdI\x91\xab\x03=\xa0\xd8\xa8\xdd}\x0e\xaey^\x94\x06V"
            b"X\xd3\xf2\xe3\xd0\x82\xe1U\xe0\x17\xd6\x97Yn\xd6\x9bu,\xb9\xd9"
            b"\xa2\xb9\x01\x00\xfb\xe5\x7f\x7f\xf7\xbc\x97\x97\x9b\xdd\xb5\xf5\xcb{\xfe~"
            b"\xfd\xcfQ\xffX\x7fP\xac\xcd1\x9d\xff\xb6\xbb\x9b\xd3=\xbe\x93\xd7"
            b'\xee\xf1\xd3\xe2\xd4\x96\xdb\x1b"I\xfd}W=\xc5\xc9\xaf\x86\xf9&\x17?\xdf\xec'
            b"7\xbd\xed\xd0\xf2\xfb\xad\xe4U\x8f\xdf,\xdbo\xdd\x1fz\xff\xff\xed"
            b"\xf2\x97o\x9d\x9f~\xf6[\x7f\xeb\xffG\xc4\xed{\x97\xbe\xfd]\xf3"
            b"\xde\xf9\xdd\xae\xffW\xd7\xbe\xb9\xbf8\xdf\xba{\xdf\xfe\nV?\xde~\xab\xf7\xbe"
            b"\xb3\xe9\xef\xa1y\x9e\xf3\xe3\xfb-\x1f\xfc\xe4\xdfE\xdbm\xdb\xff\xb7"
            b"\xdc\xb6\xec\x99{\xb8\x91\xba~\xf7\xd7~\xbf\xd4Z\xfe\xd7\xae\xf5\xe9"
            b"?\xea\xe8\xbe\x9fY[\xf6\xfe\xf7l-n\xef\x9eC\xe7\xfbCu\xfb\xef\x17\xfb"
            b"r\xdf\xbe\xffm\xdbsw\t^\x1e\xf1'v\xdb\xd7\xdf\xef\x95\xd6\x8c\xe8\xffK"
            b"\xdc\xab\xff\x17\x19\xbcu\xff\xfd\x1b\x7f\x8b\xb1\xfc\xa3{\xca\xeb{\xa7"
            b"\x1b\xaf\xdfw\xf2\xad\x7f\xd7\xfeg\xef\x11\xa6o\x1bvG~\xff\xef\xea\xb6X\xf1"
            b"\x874\x80`e#\xb7\x0c\x83\xe1/\xfe\x84\x01\xc9\xc3\x80\x84\x01\xc9"
            b"\x82\x1a\x84b|MS\x8aus-west1-7\xa0s\xc9\xd5\x11\xdb\xe5\xe9#\x11"
            b"\xf4\xcc\x13v1\xe1\x7f\x9eu\xc8m\xcd\xb4\xc9\xbc\xad\x02\x7f\xef\x15"
            b"\x86T\xf0\x88\x1bu\x0f\x02D2\x9d\xe4\x85\x15'q\x97\xab"
        ),
    ),
    HexBytes("0x720704f3aa11c53cf344ea069db95cecb81ad7453c8f276b2a1062979611f09c"): (
        b"\x00r\x07\x04\xf3\xaa\x11\xc5<\xf3D\xea\x06\x9d\xb9\\\xec\xb8\x1a\xd7E<\x8f'k*\x10b\x97\x96\x11\xf0\x9c",  # noqa: E501
        (
            b"\xf9\x02\"\xa0,X\xe3!,\x08Qx\xdb\xb1'~/<$\xb3\xf4Q&zu\xa24\x94\\\x15\x81\xaf"
            b"c\x9fJz\xa0X\xa6\x94!.\x04\x165:M8e\xcc\xf4uIkU\xaf:=;\x00 W\x00\x07"
            b"A\xaf\x971\x91\x94\x00\x19/\xb1\r\xf3|\x9f\xb2h)\xeb,\xc6#\xcd\x1b\xf5"
            b"\x99\xe8\xa0g\xa9\xfbc\x1fEy\xf9\x01^\xf3\xc6\xf1\xf3\x83\r\xfa-\xc0\x8a\xfe"
            b"\x15ou\x0e\x90\x02!4\xb9\xeb\xf6\xa0\x18\xa2\x97\x8f\xc6,\xd1\xa2"
            b">\x90\xde\x92\n\xf6\x8c\x0c:\xf33\x03'\x92|\xdaL\x00_\xac\xce\xfb\\\xe7"
            b"\xa0\x16\x8a8'`v'\xe7\x81\x94\x1d\xc7ws\x7f\xc4\xb6\xbe\xb6\x9a\x8b\x13\x92"
            b"@\xb8\x81\x99+5\xb8T\xea\xb9\x01\x00\x00 \x00\x00@\x00\x00\x00\x10\x00@\x00"
            b"\x80\x08\x00\x00\x00\x00\x00\x01\x00\x04\x01\x00\x01\x00\x00\x08"
            b"\x00\x00\x00\x00 \x00\x11\x00\x00\x00\x00\x00\x00\x00\x90\x02"
            b"\x00\x01\x11\x04\x02\x00\x80\x00\x08\x02\x08\x04\x00\x10\x00\x00"
            b'\x00\xa8\x00\x00\x00\x00\x00\x00\x00\x00\x00!\x08"\x00\t\x00 P '
            b"\x00\x00\x00\x00\x01`\x02\x00 \x00\x04\x00\x80\x00@\x00\x00\x00\x00\x00"
            b"B\x08\x00\x00\x00\x04\x00\x00@\x08\x08@ \x00\x10\x00\x00\x10\x04\x00"
            b"@\x00\x00\x10\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x11\x00"
            b"\x00\x04\x00\x00\x01\x02\x00\x84@@\x04\x81\x01\x00\x00\x08\x00 \x00@"
            b"H\x10\x08 \x02\x80\x00\x00\x10\x80 \x00\x02\x00@\x80\x08\x00\x01\x00"
            b"\x00\x00\x00\x00\x00\x00\x00  \x00\x0b\x00\x01\x00\x80`\t\x02\x00\x02"
            b"\x00\x00\x00P\x00\x04\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00 \x02\x10"
            b"\x10\x00\x00\n\x00\x00 \x00\x004 \x00\x08\x00@\x00\x00\x02\x01\x00"
            b"\x00 \x00\x00\x00\x00\x00\x00\x00\xc0\x00@\x00\x00\x01\x00\x00\x00\x10\x01"
            b"\x872{\xd7\xad1\x16\xce\x83\xe1G\xed\x84\x01\xc9\xc3d\x83\x14\r\xb1\x84b}"
            b"\x9a\xfa\x9aEthereumPPLNS/2miners_USA3\xa0\xf1\xa3.$\xebb\xf0\x1e\xc3\xf2"
            b'\xb3\xb5\x89?{\xe9\x06/\xbfT\x82\xbc\rI\nT5"@5\x0e&\x88 \x87\xfb\xb2C'
            b"2v\x96\x85\x1a\xae\x16Q\xb6"
        ),
    ),
}


def test_header_to_content(web3_block):
    content_key, content_value = block_fields_to_content(web3_block)

    # Prepare to grab expected results
    assert web3_block.hash in EXPECTED_CONTENT_BY_HASH
    expected_key, expected_value = EXPECTED_CONTENT_BY_HASH[web3_block.hash]

    assert content_key == expected_key
    assert content_value == expected_value


def test_bad_header_hash(web3_block):
    # By only changing the hash, we should see a ValidationError when trying to
    #   convert to content ID/Value
    bad_header_dict = assoc(web3_block, "hash", b"X" * 32)
    bad_header = AttributeDict(bad_header_dict)
    with pytest.raises(ValidationError):
        block_fields_to_content(bad_header)


def test_block_body_content(web3_block_and_uncles):
    web3_block, web3_uncles = web3_block_and_uncles
    content_key, content_value = encode_block_body_content(
        web3_block.transactions,
        web3_uncles,
        web3_block.hash,
        web3_block.number,
        web3_block.transactionsRoot,
        web3_block.sha3Uncles,
    )

    assert content_key == HexBytes(
        "0x01720704f3aa11c53cf344ea069db95cecb81ad7453c8f276b2a1062979611f09c"
    )  # noqa: E501
    assert HexBytes(keccak(content_value)) == HexBytes(
        "0x254346e23a1bc176de3853a33e57a6fad7712b2ef1674dd7de91b639df28dbb6"
    )  # noqa: E501


def test_bad_uncle_in_block_body_content(web3_block_and_uncles):
    web3_block, web3_uncles = web3_block_and_uncles

    wrong_reference_uncles_root = b"no" * 16
    with pytest.raises(ValidationError, match=r".*uncle.*"):
        encode_block_body_content(
            web3_block.transactions,
            web3_uncles,
            web3_block.hash,
            web3_block.number,
            web3_block.transactionsRoot,
            wrong_reference_uncles_root,
        )


def test_bad_transaction_in_block_body_content(web3_block_and_uncles):
    web3_block, web3_uncles = web3_block_and_uncles

    wrong_reference_transactions_root = b"no" * 16
    with pytest.raises(ValidationError, match=r".*transaction.*"):
        encode_block_body_content(
            web3_block.transactions,
            web3_uncles,
            web3_block.hash,
            web3_block.number,
            wrong_reference_transactions_root,
            web3_block.sha3Uncles,
        )


def test_receipt_content(web3_block_and_receipts):
    web3_block, web3_receipts = web3_block_and_receipts

    content_key, content_value = encode_receipts_content(
        web3_receipts,
        web3_block.hash,
        web3_block.number,
        web3_block.receiptsRoot,
    )

    assert content_key == HexBytes(
        "0x02720704f3aa11c53cf344ea069db95cecb81ad7453c8f276b2a1062979611f09c"
    )  # noqa: E501
    assert keccak(content_value) == HexBytes(
        "0x2d22e96ced3c0c4afd36a0d58e99dfd38f3c3a7e9b71c2127407f30730e6f599"
    )  # noqa: E501


def test_bad_receipt_content(web3_block_and_receipts):
    web3_block, web3_receipts = web3_block_and_receipts

    wrong_reference_receipt_root = b"no" * 16
    with pytest.raises(ValidationError):
        encode_receipts_content(
            web3_receipts,
            web3_block.hash,
            web3_block.number,
            wrong_reference_receipt_root,
        )
