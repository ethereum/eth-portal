from eth.vm.forks.london.blocks import LondonBlockHeader
from eth_utils import decode_hex, is_0x_prefixed, is_hexstr, remove_0x_prefix, to_hex
from flask import Flask
import rlp
from web3 import Web3

from .constants import (
    FLUFFY_BOOTNODE_ENRS,
    GREEN_CIRCLE,
    HTML_HEADER,
    RED_CIRCLE,
    TRIN_BOOTNODE_ENRS,
    ULTRALIGHT_BOOTNODE_ENRS,
)

app = Flask(__name__)

#
# Routes
#


@app.route("/")
def dashboard():
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()
    trin_bootnodes = get_trin_bootnodes_status(w3)
    fluffy_bootnodes = get_fluffy_bootnodes_status(w3)
    ultralight_bootnodes = get_ultralight_bootnodes_status(w3)
    return format_html(
        [
            "<h1> Bootnodes </h1>",
            "<h3> Trin </h3>",
            trin_bootnodes,
            "<h3> Fluffy </h3>",
            fluffy_bootnodes,
            "<h3> Ultralight </h3>",
            ultralight_bootnodes,
        ]
    )


@app.route("/header/<block_hash>")
def lookup_header(block_hash):
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()

    try:
        block_hash = format_block_hash(block_hash)
    except Exception as msg:
        return format_html(
            [
                f"<h1> Invalid block hash: {msg} </h1>",
            ]
        )

    content_key = f"0x00{block_hash}"
    try:
        result = w3.provider.make_request(
            "portal_historyRecursiveFindContent", [content_key]
        )
    except Exception:
        return format_html(
            [
                f"<h1>Looking up header: {block_hash}</h1>",
                "<p> Unable to retrieve header from network. </p>",
            ]
        )
    if "result" in result:
        ssz_bytes = result["result"]
        header = rlp.decode(decode_hex(ssz_bytes), LondonBlockHeader)
        return format_html(
            [
                f"<h1>Looking up header: {block_hash}</h1>",
                f"<p> {header.as_dict()} </p>",
            ]
        )
    else:
        return format_html([f"<p> error: {result}</p>"])


@app.route("/block_body/<block_hash>")
def lookup_body(block_hash):
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()

    try:
        block_hash = format_block_hash(block_hash)
    except Exception as msg:
        return format_html([f"<h1> Invalid block hash: {msg} </h1>"])

    content_key = f"0x01{block_hash}"
    try:
        result = w3.provider.make_request(
            "portal_historyRecursiveFindContent", [content_key]
        )
    except Exception:
        return format_html(
            [
                f"<h1>Looking up block body: {block_hash}</h1>",
                "<p> Unable to retrieve block body from network. </p>",
            ]
        )
    return format_html(
        [
            f"<h1>Looking up block body: {block_hash}</h1>",
            f"<p> {result} </p>",
        ]
    )


@app.route("/receipts/<block_hash>")
def lookup_receipts(block_hash):
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()

    try:
        block_hash = format_block_hash(block_hash)
    except Exception as msg:
        return format_html([f"<h1> Invalid block hash: {msg} </h1>"])

    content_key = f"0x02{block_hash}"
    try:
        result = w3.provider.make_request(
            "portal_historyRecursiveFindContent", [content_key]
        )
    except Exception:
        return format_html(
            [
                f"<h1>Looking up receipts: {block_hash}</h1>",
                "<p> Unable to retrieve receipts from network. </p>",
            ]
        )
    return format_html(
        [
            f"<h1>Looking up receipts: {block_hash}</h1>",
            f"<p> {result} </p>",
        ]
    )


@app.route("/eth_getBlockByNumber/<block_number>")
def eth_getBlockByNumber(block_number):
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()

    hex_block_number = to_hex(int(block_number))
    try:
        result = w3.provider.make_request(
            "eth_getBlockByNumber", [hex_block_number, False]
        )
    except Exception:
        return format_html(
            [
                f"<h1>Looking up block #{block_number}</h1>",
                "<p> Unable to retrieve block from network. </p>",
            ]
        )
    if "result" in result:
        header = result["result"]
        return format_html(
            [
                f"<h1>Looking up block #{block_number}</h1>",
                f"<p> {header} </p>",
            ]
        )
    else:
        return format_html([f"<p> error: {result}</p>"])


#
# Utils
#


def get_w3():
    return Web3(Web3.IPCProvider("/tmp/trin-jsonrpc.ipc", timeout=10))
    # return Web3(Web3.HTTPProvider("https://127.0.0.1:8545"))


def get_bootnode_status(w3, enr):
    result = w3.provider.make_request("portal_historyPing", [enr])
    enr_pretty = enr[:20]
    if "error" in result:
        return f"<p> {enr_pretty}: {RED_CIRCLE}</p>"
    return f"<p> {enr_pretty}: {GREEN_CIRCLE} </p>"


def get_trin_bootnodes_status(w3):
    statuses = [get_bootnode_status(w3, enr) for enr in TRIN_BOOTNODE_ENRS]
    return "".join(statuses)


def get_fluffy_bootnodes_status(w3):
    statuses = [get_bootnode_status(w3, enr) for enr in FLUFFY_BOOTNODE_ENRS]
    return "".join(statuses)


def get_ultralight_bootnodes_status(w3):
    statuses = [get_bootnode_status(w3, enr) for enr in ULTRALIGHT_BOOTNODE_ENRS]
    return "".join(statuses)


def format_block_hash(block_hash):
    if not is_hexstr(block_hash) or not is_0x_prefixed(block_hash):
        raise Exception("Not 0x prefixed hex.")
    block_hash = remove_0x_prefix(block_hash)
    if len(block_hash) != 64:
        return "Invalid length."
    return block_hash


def format_html(elements):
    elements.insert(0, HTML_HEADER)
    return "".join(elements)


def error_html():
    elements = [
        "<h1> Local Trin node unavailable.</h1>",
        "<p> Something's gone wrong. Please ping @nick.ghita on the Portal Network Discord.</p>",
    ]
    return format_html(elements)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
