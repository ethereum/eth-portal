Release Notes
=============

.. towncrier release notes start

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
