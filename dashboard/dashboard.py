from flask import Flask, render_template, jsonify
from web3 import Web3
from eth_utils import is_0x_prefixed, is_hexstr, remove_0x_prefix, decode_hex, to_hex, encode_hex
import rlp
from pathlib import Path

from eth.vm.forks.london.blocks import LondonBlockHeader
from eth.rlp.headers import BlockHeader

app = Flask(__name__)

#
# Routes
#


@app.route("/")
def dashboard():
    return render_template('index.html')


@app.route("/bootnodes")
def bootnodes():
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
        return {"error": "Badly formatted block hash:" + str(msg)}

    content_key = f"0x00{block_hash}"
    try:
        result = w3.provider.make_request(
            "portal_historyTraceRecursiveFindContent", [content_key]
        )
    except:
        return {"error": "Error retrieving block header."}
    if "result" in result:
        result = result["result"]
        trace = result["trace"]
        return jsonify({"result": result, "trace": trace})
    else:
        return jsonify({"error": result})


@app.route("/body/<block_hash>")
def lookup_body(block_hash):
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()

    try:
        block_hash = format_block_hash(block_hash)
    except Exception as msg:
        return {"error": "Badly formatted block hash: {msg}"}

    content_key = f"0x01{block_hash}"
    try:
        result = w3.provider.make_request(
            "portal_historyTraceRecursiveFindContent", [content_key]
        )
    except:
        return {"error": "Error retrieving block header."}
    if "result" in result:
        result = result["result"]
        trace = result["trace"]
        return jsonify({"result": result, "trace": trace})
    else:
        return jsonify({"error": result})


@ app.route("/receipts/<block_hash>")
def lookup_receipts(block_hash):
    w3 = get_w3()
    if not w3.isConnected():
        return error_html()

    try:
        block_hash = format_block_hash(block_hash)
    except Exception as msg:
        return {"error": "Badly formatted block hash: {msg}"}

    content_key = f"0x02{block_hash}"
    try:
        result = w3.provider.make_request(
            "portal_historyTraceRecursiveFindContent", [content_key]
        )
    except:
        return {"error": "Error retrieving block header."}
    if "result" in result:
        result = result["result"]
        trace = result["trace"]
        return jsonify({"result": result, "trace": trace})
    else:
        return jsonify({"error": result})


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
    except:
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
        return format_html(
            [f"<p> error: {result}</p>", ]
        )

#
# Utils
#


def get_w3():
    return Web3(Web3.IPCProvider("/tmp/trin-jsonrpc.ipc", timeout=120))
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
    print("Block hash: " + block_hash)
    if not is_hexstr(block_hash):
        raise Exception("Is not hex string.")
    if not is_0x_prefixed(block_hash):
        raise Exception("Not 0x prefixed hex.")
    block_hash = remove_0x_prefix(block_hash)
    if len(block_hash) != 64:
        return f"Invalid length."
    return block_hash


def format_html(elements):
    elements.insert(0, HTML_HEADER)
    return "".join(elements)


def error_html():
    elements = [
        "<h1> Local Trin node unavailable.</h1>",
        "<p> Looks like something's gone wrong. Please ping @nick.ghita on the Portal Network Discord. </p>",
    ]
    return format_html(elements)

#
# Constants
#


TRIN_BOOTNODE_ENRS = [
    "enr:-IS4QBISSFfBzsBrjq61iSIxPMfp5ShBTW6KQUglzH_tj8_SJaehXdlnZI-NAkTGeoclwnTB-pU544BQA44BiDZ2rkMBgmlkgnY0gmlwhKEjVaWJc2VjcDI1NmsxoQOSGugH1jSdiE_fRK1FIBe9oLxaWH8D_7xXSnaOVBe-SYN1ZHCCIyg",
    "enr:-IS4QPUT9hwV4YfNTxazR2ltch4qKzvX_HwxQBw8gUN3q1MDfNyaD1EHc1wQZRTUzQQD-RVYx3h4nA1Sqk0Wx9DwzNABgmlkgnY0gmlwhM69ZOyJc2VjcDI1NmsxoQLaI-m2CDIjpwcnUf1ESspvOctJLpIrLA8AZ4zbo_1bFIN1ZHCCIyg",
    "enr:-IS4QB77AROcGX-TSkY-U-SaZJ5ma9ICQj6ETO3FqUdCnTZeJ0mDrdCKUqd5AQ0jrHa7m9-mOLvFFKMV_-tBD8uDYZUBgmlkgnY0gmlwhJ_fCDaJc2VjcDI1NmsxoQN9rahqamBOJfj4u6yssJQJ1-EZoyAw-7HIgp1FwNUdnoN1ZHCCIyg",
]

FLUFFY_BOOTNODE_ENRS = [
    "enr:-IS4QGeTMHteRmm-MSYniUd48OZ1M7RMUsIjnSP_TRbo-goQZAdYuqY2PyNJfDJQBz33kv16k7WB3bZnBK-O1DagvJIBgmlkgnY0gmlwhEFsKgOJc2VjcDI1NmsxoQIQXNgOCBNyoXz_7XP4Vm7pIB1Lp35d67BbC4iSlrrcJoN1ZHCCI40",
    "enr:-IS4QOA4voX3J7-R_x8pjlaxBTpT1S_CL7ZaNjetjZ-0nnr2VaP0wEZsT2KvjA5UWc8vi9I0XvNSd1bjU0GXUjlt7J0BgmlkgnY0gmlwhEFsKgOJc2VjcDI1NmsxoQI7aL5dFuHhwbxWD-C1yWH7UPlae5wuV_3WbPylCBwPboN1ZHCCI44",
    "enr:-IS4QFzPZ7Cc7BGYSQBlWdkPyep8XASIVlviHbi-ZzcCdvkcE382unsRq8Tb_dYQFNZFWLqhJsJljdgJ7WtWP830Gq0BgmlkgnY0gmlwhEFsKq6Jc2VjcDI1NmsxoQPjz2Y1Hsa0edvzvn6-OADS3re-FOkSiJSmBB7DVrsAXIN1ZHCCI40",
    "enr:-IS4QHA1PJCdmESyKkQsBmMUhSkRDgwKjwTtPZYMcbMiqCb8I1Xt-Xyh9Nj0yWeIN4S3sOpP9nxI6qCCR1Nf4LjY0IABgmlkgnY0gmlwhEFsKq6Jc2VjcDI1NmsxoQLMWRNAgXVdGc0Ij9RZCPsIyrrL67eYfE9PPwqwRvmZooN1ZHCCI44",
]

ULTRALIGHT_BOOTNODE_ENRS = [
    "enr:-IS4QFV_wTNknw7qiCGAbHf6LxB-xPQCktyrCEZX-b-7PikMOIKkBg-frHRBkfwhI3XaYo_T-HxBYmOOQGNwThkBBHYDgmlkgnY0gmlwhKRc9_OJc2VjcDI1NmsxoQKHPt5CQ0D66ueTtSUqwGjfhscU_LiwS28QvJ0GgJFd-YN1ZHCCE4k",
    "enr:-IS4QDpUz2hQBNt0DECFm8Zy58Hi59PF_7sw780X3qA0vzJEB2IEd5RtVdPUYZUbeg4f0LMradgwpyIhYUeSxz2Tfa8DgmlkgnY0gmlwhKRc9_OJc2VjcDI1NmsxoQJd4NAVKOXfbdxyjSOUJzmA4rjtg43EDeEJu1f8YRhb_4N1ZHCCE4o",
    "enr:-IS4QGG6moBhLW1oXz84NaKEHaRcim64qzFn1hAG80yQyVGNLoKqzJe887kEjthr7rJCNlt6vdVMKMNoUC9OCeNK-EMDgmlkgnY0gmlwhKRc9-KJc2VjcDI1NmsxoQLJhXByb3LmxHQaqgLDtIGUmpANXaBbFw3ybZWzGqb9-IN1ZHCCE4k",
    "enr:-IS4QA5hpJikeDFf1DD1_Le6_ylgrLGpdwn3SRaneGu9hY2HUI7peHep0f28UUMzbC0PvlWjN8zSfnqMG07WVcCyBhADgmlkgnY0gmlwhKRc9-KJc2VjcDI1NmsxoQJMpHmGj1xSP1O-Mffk_jYIHVcg6tY5_CjmWVg1gJEsPIN1ZHCCE4o",
]

HTML_HEADER = """
    <h1> Portal Network </h1>
    <a href='/'>Home</a>
    <h2> How to use this site </h2>
    <li> <code>/header/[0x-prefixed-block-hash]</code> : to lookup a block header </li>
    <li> <code>/block_body/[0x-prefixed-block-hash]</code> : to lookup a block body </li>
    <li> <code>/receipts/[0x-prefixed-block-hash]</code> : to lookup a block's receipts </li>
    <li> <code>/eth_getBlockByNumber/[block_number]</code> : to lookup a pre-merge block </li>
    <li> <code>/eth_getBlockByHash/[0x-prefixed-block-hash]</code> : to lookup a block </li>
    <br>
    <h3> Data Availability </h3>
    <p>
        The Portal Network is still in unstable alpha. It might be difficult to reliably retrieve any
        particular piece of data until the network stabilizes. 
    </p>
    <p>
        If you're having trouble retrieving content,
        try `eth_getBlockByHash` for a recently mined block, since the bridge nodes are most likely to inject
        recent blocks into the network.
    </p>
    <hr>
"""
RED_CIRCLE = "&#x1F534;"
GREEN_CIRCLE = "&#128994;"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
