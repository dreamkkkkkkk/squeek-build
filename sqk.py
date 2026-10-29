#!/usr/bin/env python3
"""Minimal Squeekchain (Sepolia) client. Read-only by default."""
import json, os, sys, urllib.request

RPC = os.environ.get("SEPOLIA_RPC", "https://ethereum-sepolia-rpc.publicnode.com")
C = {
    "core":     "0x980b4424c007caf7a1f3670b48c8eaef7ebc3d44",
    "token":    "0x5501e1fa81be1c3f49225fa7668da0245d07db60",
    "mining":   "0xcd46990f8349057335289ef282c276204b6cdc62",
    "staking":  "0x4b67b739dfd832f4eac67a7aa3bc244fb74cea4f",
    "genesis":  "0xcb98349c134ab983da5bfd80527dfe2552bdb70f",
    "factory":  "0x779a302adbaa9c8a3da45ef48ad67e6a45fcef29",
    "launch":   "0x1ff6485abfbb2d183cd673d78e1ab31c098e04dd",
    "gacha":    "0x5f6ba50f448b84e09f5ee324a6402b033ba70e28",
}
# zero-arg selectors that return data on-chain (see docs/selectors.md)
PING = {"genesis": "0x18160ddd", "launch": "0x3c8463a1",
        "gacha": "0xfc0c546a", "core": "0x5c975abb", "token": "0x18160ddd"}


def rpc(method, params):
    req = urllib.request.Request(
        RPC,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
        headers={"content-type": "application/json", "user-agent": "curl/8.7.1"},
    )
    out = json.load(urllib.request.urlopen(req, timeout=30))
    if "error" in out:
        raise SystemExit(out["error"])
    return out["result"]


def call(to, data):
    return rpc("eth_call", [{"to": to, "data": data}, "latest"])


def info():
    sym = bytes.fromhex(call(C["token"], "0x95d89b41")[2:]).rstrip(b"\x00")[32:].decode(errors="ignore")
    sup = int(call(C["token"], "0x18160ddd"), 16)
    gen = int(call(C["genesis"], "0x18160ddd"), 16)
    print(f"SQK symbol={sym!r} totalSupply={sup/1e18:,.2f}")
    print(f"genesis count={gen}")


def ping(name):
    from eth_account import Account
    pk = os.environ.get("PK")
    if not pk:
        raise SystemExit("export PK=0x... first")
    acct = Account.from_key(pk)
    to = C[name]
    data = PING[name]
    gas = int(rpc("eth_estimateGas", [{"from": acct.address, "to": to, "data": data}]), 16)
    price = int(rpc("eth_gasPrice", []), 16)
    tx = {
        "chainId": 11155111,
        "nonce": int(rpc("eth_getTransactionCount", [acct.address, "pending"]), 16),
        "to": bytes.fromhex(to[2:]), "value": 0, "data": data,
        "gas": gas + 5000, "maxFeePerGas": price * 2,
        "maxPriorityFeePerGas": max(1, price // 2), "type": 2,
    }
    s = Account.sign_transaction(tx, pk)
    raw = getattr(s, "raw_transaction", None) or s.rawTransaction
    h = rpc("eth_sendRawTransaction", ["0x" + (raw.hex() if isinstance(raw, bytes) else raw)])
    print("sent", h)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "info"
    if cmd == "info":
        info()
    elif cmd == "ping":
        ping(sys.argv[2])
    else:
        raise SystemExit("usage: sqk.py info | ping <core|token|mining|staking|genesis|factory|launch|gacha>")
