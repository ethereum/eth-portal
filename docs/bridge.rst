Run a Bridge Node
=========================

Bridge Node Intro
------------------------

A bridge node for the Portal Network is responsible for pushing new data into
the network. It doesn't require any special authority. Anyone can run a bridge
node.

It starts by monitoring the Ethereum network and storing newfound data into a
Portal client that has joined the network, using a Portal-specific json-rpc API,
like ``portal_historyOffer``. See the full `Portal RPC API
<https://playground.open-rpc.org/?schemaUrl=https://raw.githubusercontent.com/ethereum/portal-network-specs/assembled-spec/jsonrpc/openrpc.json&uiSchema%5BappBar%5D%5Bui:splitView%5D=false&uiSchema%5BappBar%5D%5Bui:input%5D=false&uiSchema%5BappBar%5D%5Bui:examplesDropdown%5D=false>`_.

When to Run a Bridge Node
---------------------------

You likely don't need to. You probably just want to run a Portal Client. If
you have high uptime needs, maybe you should run an execution client like geth.
A bridge node is just a weird artifact of how the Portal Network works, and
most folks can ignore it.

How to Run a Bridge Node
--------------------------

First Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use this bash code to launch the bridge for the very first time::

  # If you put this code block into a bash script, then the following line will
  #   cause the script to exit early if any variable is missing
  set -o nounset

  # Install a fresh virtualenv, to have a clean installation environment
  python3 -m venv eth-portal-venv

  # Enter the new virtualenv environment
  . eth-portal-venv/bin/activate

  # Make sure to use the latest pip & setuptools
  pip install -U pip setuptools

  # Install eth-portal
  pip install eth-portal

  # Link to your already-built trin binary
  ln -s $PATH_TO_TRIN_BINARY trin

  # Verify that the Infura ID is provided
  [ "$WEB3_INFURA_PROJECT_ID" ] || echo "Missing Infura project ID!"

  # Verify that some trin private keys are provided
  [ "$PORTAL_BRIDGE_KEYS" ] || echo "Missing Portal Bridge Keys!"

  # Launch the bridge node
  python -m eth_portal.bridge

.. note::
  Look for the ALL_CAPS variables that you must provide ahead of time with
  ``export``.

Run after first installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you exit your terminal and want to restart the bridge node, you can relaunch
with::

  # Navigate to the directory that eth-portal was orignally installed in

  # Launch virtalenv
  . eth-portal-venv/bin/activate

  # Launch the bridge node
  python -m eth_portal.bridge

You can find more detail about these steps in the sections below.

Detail on eth-portal Install
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a fresh virtualenv, run ``pip install eth-portal`` to install.

If you want to instead use the latest, greatest (and potentially buggiest),
check out `eth-portal <https://github.com/carver/eth-portal>`_ via git and
install dependencies with ``pip install -e .[dev]``.

Detail on Linking to trin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bridge launches a bunch of portal clients, in order to join into the
network with peers that have a variety of different node IDs. In theory, the
bridge can work with any Portal client, but for now, it is hard-coded to
``trin``.

Get a copy of the ``trin`` binary. A straightforward approach is to check out trin
from source and run ``cargo build``.  Then, place the binary of ``trin`` in
the root of the eth-portal source directory.

For example, if trin is checked out in a sibling directory to eth-portal, you
could run this from the parent directory of both::

    ln -s trin/target/debug/trin eth-portal/trin

Detail on Linking to Infura
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bridge currently uses Infura to track when new headers arrive.
Eventually, this will switch to using an execution client like geth.

For now, create an Infura project and add the ID as an environment variable::

    export WEB3_INFURA_PROJECT_ID=1234567890abcdef

Detail on Portal Bridge Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bridge requires private keys to launch the Portal clients. There is some
subtletly in choosing these keys ideally, but it's probably fine to just pick a
bunch at random. How many is the ideal number to run? It is still an open
question.

After selecting your private keys, concatenate them using commas and add it to your environment::

    export PORTAL_BRIDGE_KEYS=7261696e626f77737261696e626f77737261696e626f77737261696e626f7773,756e69636f726e73756e69636f726e73756e69636f726e73756e69636f726e73


Detail on Launching the Bridge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have any trouble launching the bridge::

    python -m eth_portal.bridge

Then first make sure that you have activated your virtualenv, and are in the
originally installed directory. There should be a ``trin`` binary linked there.

It's currently assumed that the ``/tmp`` is available, and the ports 9000, 9001,
etc. are available. For each trin key you provide, the bridge will launch
another instance of trin, which will use another port.

Running the bridge will use about 650k requests a day, at current mainnet levels.
That requires a paid Infura account to run full-time.


How to See the trin Logs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One way to see the logs being emitted from trin is to run trin manually and
set RUST_LOG to display the desired logging level. The bridge will notice that
trin is already running, and use that instance.

In order to determine the correct trin command, you can inspect the shell
output at the beginning of launching the bridge. Then shut down the bridge, use
the printed command to launch trin, and re-launch the bridge.
