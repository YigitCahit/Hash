from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from hash import chain_hash_64

DEFAULT_STORE = Path("text_chain.json")
Block = Dict[str, object]

def load_chain(store: Path) -> List[Block]:
    if not store.exists():
        return []
    raw = store.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Chain file {store} is corrupted: {exc}")
    if not isinstance(data, list):
        raise SystemExit(f"Chain file {store} must contain a list of blocks")
    return data

def save_chain(chain: List[Block], store: Path) -> None:
    store.write_text(json.dumps(chain, indent=2), encoding="utf-8")

def canonical_payload(index: int, timestamp: str, text: str, prev_hash: str) -> str:
    return f"{index}|{timestamp}|{text}|{prev_hash}"

def compute_hash(index: int, timestamp: str, text: str, prev_hash: str) -> str:
    payload = canonical_payload(index, timestamp, text, prev_hash)
    return chain_hash_64(payload)

def new_block(text: str, prev_block: Block | None) -> Block:
    index = 0 if prev_block is None else int(prev_block["index"]) + 1
    prev_hash = "0" * 64 if prev_block is None else str(prev_block["hash"])
    timestamp = datetime.now(timezone.utc).isoformat()
    block_hash = compute_hash(index, timestamp, text, prev_hash)
    return {
        "index": index,
        "timestamp": timestamp,
        "text": text,
        "prev_hash": prev_hash,
        "hash": block_hash,
    }

def ensure_genesis(chain: List[Block]) -> List[Block]:
    if chain:
        return chain
    genesis = new_block("GENESIS", None)
    return [genesis]

def append_text(text: str, store: Path) -> Block:
    chain = load_chain(store)
    chain = ensure_genesis(chain)
    last_block = chain[-1]
    block = new_block(text, last_block)
    chain.append(block)
    save_chain(chain, store)
    return block

def verify_chain(chain: List[Block]) -> Tuple[bool, str]:
    if not chain:
        return False, "Chain is empty"
    for idx, block in enumerate(chain):
        if idx == 0:
            expected_prev = "0" * 64
        else:
            expected_prev = str(chain[idx - 1]["hash"])
        if str(block["prev_hash"]) != expected_prev:
            return False, f"Block {idx} has invalid prev_hash"
        recomputed = compute_hash(
            int(block["index"]), str(block["timestamp"]), str(block["text"]), str(block["prev_hash"])
        )
        if recomputed != block["hash"]:
            return False, f"Block {idx} hash mismatch"
    return True, "Chain is valid"

def reset_chain(store: Path) -> None:
    chain = ensure_genesis([])
    save_chain(chain, store)

def list_chain(store: Path) -> List[Block]:
    chain = load_chain(store)
    if not chain:
        return []
    return chain

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple blockchain-like text storage")
    parser.add_argument(
        "--store",
        type=Path,
        default=DEFAULT_STORE,
        help=f"Path to chain storage file (default: {DEFAULT_STORE})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add_parser = sub.add_parser("add", help="Add a new text entry to the chain")
    add_parser.add_argument("text", help="Text payload to store")

    sub.add_parser("list", help="List all text entries")
    sub.add_parser("verify", help="Verify chain integrity")
    sub.add_parser("reset", help="Reset the chain with a new genesis block")

    return parser.parse_args()

def main() -> None:
    args = parse_args()
    store: Path = args.store

    if args.command == "add":
        block = append_text(args.text, store)
        print(f"Block {block['index']} added with hash {block['hash']}")
    elif args.command == "list":
        chain = list_chain(store)
        if not chain:
            print("No blocks found. Use 'add' to create the genesis entry.")
            return
        for block in chain:
            text = str(block["text"])
            snippet = text if len(text) < 60 else text[:57] + "..."
            print(f"#{block['index']} @ {block['timestamp']} -> {snippet}")
    elif args.command == "verify":
        chain = load_chain(store)
        ok, msg = verify_chain(chain)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {msg}")
    elif args.command == "reset":
        reset_chain(store)
        print(f"Chain reset at {store}")

if __name__ == "__main__":
    main()
