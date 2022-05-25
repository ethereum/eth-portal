from contextlib import contextmanager
from pathlib import Path
import signal
import subprocess

from eth_keys.datatypes import PrivateKey
from eth_utils import keccak, remove_0x_prefix
from web3 import Web3


# TODO set data directory into a ramdisk to avoid disk contention
#   especially when running >> 8 nodes
@contextmanager
def launch_trin(private_key: bytes, port: int):
    """
    Launch an instance of trin, yield a configured web3 & exit when context ends.

    Modify the IPC path so that several nodes can run simultaneously, assuming
    their first 10 bytes of node ID are distinct.

    The point of these importer nodes is not to host the data, but to broadcast
    it. So keep a small cap on the data storage of 20 MB. 256 nodes * 20MB
    would be only 5GB, which could fit on a ramdisk.
    """
    public_key = PrivateKey(private_key).public_key.to_bytes()
    node_id_hex = keccak(public_key).hex()
    ipc_path = f"/tmp/trin-jsonrpc-{node_id_hex[:20]}.ipc"
    private_key_hex = remove_0x_prefix(private_key.hex())

    short_node_id = node_id_hex[:10]
    trin_args = [
        "./trin",
        # fmt: off
        "--discovery-port", str(port),
        "--unsafe-private-key", private_key_hex,
        "--web3-ipc-path", ipc_path,
        "--kb", "20000",
        "--networks", "history",
        "--bootnodes", "default",
        # fmt: on
    ]

    if Path(ipc_path).exists():
        print(f"trin already running for {short_node_id}, skipping launch...")
        trin_proc = None
    else:
        print(f"Launching trin with node ID {short_node_id} using...")
        print(" ".join(trin_args))
        trin_proc = subprocess.Popen(
            trin_args,
            env={"TRIN_INFURA_PROJECT_ID": "1"},
        )

    try:
        yield Web3(Web3.IPCProvider(ipc_path))
    finally:
        if trin_proc:
            print(f"Exiting trin with node ID {node_id_hex[:10]}...")
            trin_proc.send_signal(signal.SIGINT)
            trin_proc.wait()
        else:
            print(
                f"Did not launch trin with node ID {node_id_hex[:10]}, so cannot exit."
            )
