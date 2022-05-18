Run a Bridge Node
=========================

Bridge Node Intro
------------------------

A bridge node for the Portal Network is responsible for pushing new data into
the network. It doesn't require any special authority. Anyone can run a bridge
node.

It starts by monitoring the Ethereum network and storing newfound data into a
Portal client that has joined the network, using a Portal-specific json-rpc API,
like ``portal_historyStore``. See the full `Portal RPC API
<https://playground.open-rpc.org/?schemaUrl=https://raw.githubusercontent.com/ethereum/portal-network-specs/assembled-spec/jsonrpc/openrpc.json&uiSchema%5BappBar%5D%5Bui:splitView%5D=false&uiSchema%5BappBar%5D%5Bui:input%5D=false&uiSchema%5BappBar%5D%5Bui:examplesDropdown%5D=false>`_.

When to Run a Bridge Node
---------------------------

You likely don't need to. You probably just want to run a Portal Client. If
you have high uptime needs, maybe you should run an execution client like geth.
A bridge node is just a weird artifact of how the Portal Network works, and
most folks can ignore it.

How to Run a Bridge Node
--------------------------

Install eth-portal from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check out `eth-portal <https://github.com/carver/eth-portal>`_ via git, launch
a fresh virtualenv, and install dependencies with ``pip install -e .[dev]``.

Link to a Portal Client
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

Link to Infura
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bridge currently uses Infura to track when new headers arrive.
Eventually, this will switch to using an execution client like geth.

For now, create an Infura project and add the ID as an environment variable::

    export WEB3_INFURA_PROJECT_ID=1234567890abcdef

Specify Portal Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The bridge requires private keys to launch the Portal clients. There is some
subtletly in choosing these keys ideally, but it's probably fine to just pick a
bunch at random. How many is the ideal number to run? It is still an open
question.

After selecting your private keys, concatenate them using commas and add it to your environment::

    export PORTAL_BRIDGE_KEYS=7261696e626f77737261696e626f77737261696e626f77737261696e626f7773,756e69636f726e73756e69636f726e73756e69636f726e73756e69636f726e73


Run the Bridge Launcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From within the virtualenv that eth-portal is installed, at the root of the
eth-portal directory, run::

    ./scripts/launch_bridge.py

The script will print when a new header is being pushed to the Portal clients.

It's currently assumed that ``/tmp`` is available, and the ports 9000, 9001,
etc. are available (depending on how many Portal clients you launch).

This will roughly use up a full free Infura account.
