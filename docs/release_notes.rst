Release Notes
=============

.. towncrier release notes start

Portal Network Tools v0.2.1 (2022-10-04)
----------------------------------------


Features
~~~~~~~~

- Updated content key encoding ssz scheme & test vectors to new spec, removing the chain id. (`#44 <https://github.com/ethereum/eth-portal/issues/44>`__)


Bugfixes
~~~~~~~~

- Correct the maximum receipt length in SSZ encoding. No specific bug is known to be fixed by this change. (`#40 <https://github.com/ethereum/eth-portal/issues/40>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Update ``ln -s`` example in bridge setup guide to use absolute source path. This prevents folks from
  getting a ``Too many levels of symbolic links`` error during setup, because `soft links require an
  absolute source path <https://unix.stackexchange.com/a/180532/251234>`_. (`#42 <https://github.com/ethereum/eth-portal/issues/42>`__)


Portal Network Tools v0.2.0 (2022-09-22)
----------------------------------------


Breaking changes
~~~~~~~~~~~~~~~~

- In order to follow the tip of the chain, you must now specify ``--latest`` or ``-l``.
  See "Run after first installation" under "Run a Bridge Node" (`#38 <https://github.com/ethereum/eth-portal/issues/38>`__)


Features
~~~~~~~~

- Publish data from a historical block range with ``--block-range``. See "Backfill historical blocks" under "Run a Bridge Node" (`#34 <https://github.com/ethereum/eth-portal/issues/34>`__)
- Add the ability to inject specific content items on-demand with ``--content-files``. See "Inject content manually" under "Run a Bridge Node" (`#35 <https://github.com/ethereum/eth-portal/issues/35>`__)


Internal Changes - for Portal Network Tools Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- When receipts fail their check against the expected root hash, save them to a file in a temporary
  directory (`#32 <https://github.com/ethereum/eth-portal/issues/32>`__)


Miscellaneous changes
~~~~~~~~~~~~~~~~~~~~~

- Merge in latest project template `#41 <https://github.com/ethereum/eth-portal/issues/41>`__


Portal Network Tools v0.1.0 (2022-08-31)
----------------------------------------

Features
~~~~~~~~

- Officially claim support for python versions up to 3.9 (won't support 3.10 until a stable web3
  version does...) (`#29 <https://github.com/ethereum/eth-portal/issues/29>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Add a compiled first-time install script to docs (`#25 <https://github.com/ethereum/eth-portal/issues/25>`__)


Internal Changes - for Portal Network Tools Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- - Upgrade ssz to v0.3.0 to get cleaner & faster ssz bytelist decoding
  - Apply ``black`` formatting to setup.py (`#29 <https://github.com/ethereum/eth-portal/issues/29>`__)
- Update project template to get smaller releases, a towncrier duplicate-note fix, CircleCI image
  upgrade, breaking change newsfragments, and pydocstyle failure explanations. (`#30 <https://github.com/ethereum/eth-portal/issues/30>`__)


Miscellaneous changes
~~~~~~~~~~~~~~~~~~~~~

- `#28 <https://github.com/ethereum/eth-portal/issues/28>`__


Breaking changes
~~~~~~~~~~~~~~~~

- Use the portal_historyOffer rpc endpoint of trin, instead of portal_historyStore. This requires a
  more recent version of trin. Follow the `rpc update in trin
  <https://github.com/ethereum/trin/pull/411>`_ for more. (`#27 <https://github.com/ethereum/eth-portal/issues/27>`__)
- Drop Python3.6 to support the latest ssz v0.3.0, which doesn't support py3.6. (`#29 <https://github.com/ethereum/eth-portal/issues/29>`__)


Portal Network Tools v0.1.0-beta.0 (2022-06-02)
-----------------------------------------------

Features
~~~~~~~~

- Launch the bridge with ``python -m eth_portal.bridge``. (`#23 <https://github.com/ethereum/eth-portal/issues/23>`__)
- Add a new script to monitor new headers, with Infura. Also, add utility to encode header fields
  into serialized RLP object. (`#1 <https://github.com/ethereum/eth-portal/issues/1>`__)
- Encode header hash into a Portal History Network content key (`#2 <https://github.com/ethereum/eth-portal/issues/2>`__)
- Encode header content key & value, on each new header hash.  (`#3 <https://github.com/ethereum/eth-portal/issues/3>`__)
- Launch trin nodes with bridge, and push content to them, as new headers arrive. (`#4 <https://github.com/ethereum/eth-portal/issues/4>`__)
- Encode the content key for block receipts (`#7 <https://github.com/ethereum/eth-portal/issues/7>`__)
- Encode receipt values, tested against header's receipt root hash (`#8 <https://github.com/ethereum/eth-portal/issues/8>`__)
- Encode a group of receipts to its Portal Network content value. Currently assumes that we
  switch to using an SSZ list from the RLP list. (`#10 <https://github.com/ethereum/eth-portal/issues/10>`__)
- Push the block's receipts out to trin nodes, after detecting a new header. (`#11 <https://github.com/ethereum/eth-portal/issues/11>`__)
- In bridge launcher, detect if trin "injector" node is already running, then use it. One benefit is
  being able to observe the logs on trin during bridge operation. (`#14 <https://github.com/ethereum/eth-portal/issues/14>`__)
- Encode the content key for block bodies (`#16 <https://github.com/ethereum/eth-portal/issues/16>`__)
- Decode a web3 transaction into a py-evm one, for encoding & hashing (`#17 <https://github.com/ethereum/eth-portal/issues/17>`__)
- Encode uncles and transactions into a block body for Portal Network. (`#18 <https://github.com/ethereum/eth-portal/issues/18>`__)
- Propagate block bodies on the Portal History Network. (`#19 <https://github.com/ethereum/eth-portal/issues/19>`__)


Improved Documentation
~~~~~~~~~~~~~~~~~~~~~~

- Add `bridge` node guide (`#4 <https://github.com/ethereum/eth-portal/issues/4>`__)


Internal Changes - for Portal Network Tools Contributors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Add web3 dependency in order to poll for new headers, and py-evm dependency to encode headers to RLP (`#1 <https://github.com/ethereum/eth-portal/issues/1>`__)
- Use black as the code formatter, and add to CI for enforcement. Upgrade isort to v5 for
  compatibility. (`#12 <https://github.com/ethereum/eth-portal/issues/12>`__)


v0.1.0-alpha.1
--------------

- Added a script to generate private keys and Node IDs
- Launched repository, claimed names for pip, RTD, github, etc
