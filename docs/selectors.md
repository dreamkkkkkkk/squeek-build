# Recovered selectors (runtime bytecode)

The core, mining and staking deployments are EIP-1967-style proxies whose
implementations are not verified on Etherscan or Sourcify, so these selectors were
recovered by scanning `PUSH4` immediates in the runtime bytecode and replaying each
one through `eth_call` with no arguments. Values are what the chain returned on
2026-10-29 (Sepolia block 12020000).

## genesis `0xcb98349c…db70f`

| selector | returns |
|---|---|
| `0x18160ddd` | `9999` (member places) |
| `0x01339c21` | `0x1ff6485abfbb2d183cd673d78e1ab31c098e04dd` (launch) |
| `0x3c3da587` | `0x980b4424c007caf7a1f3670b48c8eaef7ebc3d44` (core) |
| `0x452a9320` | `0x3c4c2ba9a5dfbfc5e48dceabdd3b004131a04be6` (guardian) |
| `0x32cb6b0c` | `9999` |
| `0x2281bea2`* | name() -> "Squeek" |

## launch `0x1ff6485a…04dd`

| selector | returns |
|---|---|
| `0x3c8463a1` | `20` |
| `0x47ccca02` | `0xcb98349c134ab983da5bfd80527dfe2552bdb70f` (genesis) |
| `0xd54ad2a1` / `0xe3177e6b` | `8888` |
| `0xf2f4eb26` | `0x980b4424…` (core) |

## gachaVault `0x5f6ba50f…0e28`

| selector | returns |
|---|---|
| `0xfc0c546a` | `0x5501e1fa81be1c3f49225fa7668da0245d07db60` (SQK) |
| `0xc3fe3e28` | `0x81b56d54d2ade6a1bea097792b17138e34eec761` |

## core implementation `0x284747c4…e6889`

`0x5c975abb` returns `0` (not paused); `0xe5900225` returns `3`;
`0x85fabc21` returns the current stream digest.
