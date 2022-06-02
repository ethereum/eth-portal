from ssz.sedes import Byte, Container, List, Vector, uint8, uint16

#
# History Network Sedes
#

# Content Key serializations
HEADER_TYPE_BYTE = b"\x00"
BODY_TYPE_BYTE = b"\x01"
RECEIPT_TYPE_BYTE = b"\x02"
BLOCK_KEY_SEDES = Container(
    (
        uint16,  # Chain ID
        Vector(uint8, 32),  # header hash
    )
)

# Content Value serializations

_MAX_TRANSACTION_LENGTH = 2**24  # ~= 16 million
# Maximum transaction body length is achieved by filling calldata with 0's
# until the block limit of 30M gas is reached.
# At a gas cost of 4 per 0-byte, that produces a 7.5MB transaction. We roughly
# double that size to a maximum of >16 million for some headroom. Note that
# EIP-4488 would put a roughly 1MB limit on transaction length, effectively. So
# increases are not planned (instead, the opposite).

_MAX_TRANSACTION_COUNT = 2**14  # ~= 16k
# 2**14 simple transactions would use up >340 million gas at 21k gas each.
# Current gas limit tops out at 30 million gas.

_MAX_RECEIPT_LENGTH = 2**23  # ~= 8 million
# Maximum receipt length is logging a bunch of data out, currently at a cost of
# 8 gas per byte. Since that is double the cost of 0 calldata bytes, the
# maximum size is roughly half that of the transaction. That gives a maximum of
# >8 million bytes per receipt.

_MAX_HEADER_LENGTH = 2**13  # = 8192
# Maximum header length is fairly stable at about 500 bytes. It might change at
# the merge, and beyond. Since the length is relatively small, and the future
# of the format is unclear to me, I'm leaving more room for expansion, and
# setting the max at about 8 kilobytes.

_MAX_ENCODED_UNCLES_LENGTH = _MAX_HEADER_LENGTH * 2**4  # = 2**17 ~= 131k
# Maximum number of uncles is currently 2. Using 16 leaves some room for the
# protocol to increase the number of uncles.

_TRANSACTIONS_SEDES = List(
    # Each encoded transaction
    List(Byte(), _MAX_TRANSACTION_LENGTH),
    _MAX_TRANSACTION_COUNT,
)
_UNCLES_SEDES = List(
    # The combined rlp-encoded list of headers
    Byte(),
    _MAX_ENCODED_UNCLES_LENGTH,
)
BLOCK_BODY_SEDES = Container((_TRANSACTIONS_SEDES, _UNCLES_SEDES))

BLOCK_RECEIPTS_SEDES = List(
    # Each encoded receipt
    List(Byte(), _MAX_RECEIPT_LENGTH),
    _MAX_TRANSACTION_COUNT,
)
