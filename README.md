# SQK Toolkit

A small, dependency-light toolkit for working with the **Squeekchain** contracts on
Ethereum Sepolia (`chainId 11155111`).

Squeekchain is a proof-of-work chain whose work units are produced by physical
hardware, with an on-chain economy for mining, staking and a Genesis member
program. This repo collects the pieces I use to read that economy and to talk to
its contracts directly.

## Contracts (Sepolia)

| role        | address |
|-------------|---------|
| core        | `0x980b4424c007caf7a1f3670b48c8eaef7ebc3d44` |
| token (SQK) | `0x5501e1fa81be1c3f49225fa7668da0245d07db60` |
| mining      | `0xcd46990f8349057335289ef282c276204b6cdc62` |
| staking     | `0x4b67b739dfd832f4eac67a7aa3bc244fb74cea4f` |
| genesis     | `0xcb98349c134ab983da5bfd80527dfe2552bdb70f` |
| tokenFactory| `0x779a302adbaa9c8a3da45ef48ad67e6a45fcef29` |
| launch      | `0x1ff6485abfbb2d183cd673d78e1ab31c098e04dd` |
| gachaVault  | `0x5f6ba50f448b84e09f5ee324a6402b033ba70e28` |

## Contents

- `sqk.py` — minimal client: reads ERC-20 state and can send a zero-value call
  to any tracked contract (useful as a connectivity / indexing smoke test).
- `docs/selectors.md` — function selectors recovered from the deployed bytecode
  of the unverified contracts, with the values observed from `eth_call`.

## Usage

```bash
export SEPOLIA_RPC=https://ethereum-sepolia-rpc.publicnode.com
python3 sqk.py info            # read-only: symbol / supply / genesis count
python3 sqk.py ping genesis    # send a zero-value call to a tracked contract
```

`ping` needs a funded key: `export PK=0x...`

## Notes

The core, mining and staking deployments are proxies; their implementations were
not published to Etherscan, so the selectors in `docs/selectors.md` were recovered
directly from runtime bytecode. Behaviour described there is what the chain
actually returns, not what the docs claim.
