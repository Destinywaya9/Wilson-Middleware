#!/usr/bin/env python3
import argparse, csv, hashlib, json
from pathlib import Path


def normalize(v):
    if v is None:
        return ""
    s = str(v)
    low = s.lower()
    if low == "true": return True
    if low == "false": return False
    if low in ("nan", "none", ""): return s if s == "" else s
    try:
        if any(ch in s for ch in ".eE"):
            return float(s)
        return int(s)
    except Exception:
        return s


def canonical_hash(obj):
    payload = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def verify_chain(rows, prev_key, hash_key, genesis="GENESIS"):
    prev = genesis
    for i, row in enumerate(rows):
        if row[prev_key] != prev:
            return False, f"row {i}: prev hash mismatch"
        d = {k: normalize(v) for k, v in row.items() if k != hash_key}
        got = canonical_hash(d)
        if got != row[hash_key]:
            return False, f"row {i}: row hash mismatch"
        prev = row[hash_key]
    return True, prev


def canonical_policy_hash(path):
    policy = json.loads(path.read_text(encoding="utf-8"))
    payload = json.dumps(policy, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def as_bool(v):
    return str(v).strip().lower() == "true"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("output_dir", nargs="?", default="qtet_outputs")
    args = ap.parse_args()
    out = Path(args.output_dir)
    receipt = json.loads((out / "Wilson_Public_Audit_Receipt.json").read_text())

    mw = load_csv(out / "Wilson_Middleware_Execution_Ledger.csv")
    ethics = load_csv(out / "Wilson_Ethics_Checkpoint_Ledger.csv")
    ok_mw, root_mw = verify_chain(mw, "prev_row_hash", "row_hash")
    ok_ethics, root_ethics = verify_chain(ethics, "prev_ethics_hash", "ethics_row_hash")

    qpu_path = out / "Wilson_IBM_QPU_Evidence_Ledger.csv"
    if not qpu_path.exists():
        qpu_path = out / "Wilson_QPU_Evidence_Ledger.csv"
    qpu = load_csv(qpu_path)
    ok_qpu, root_qpu = verify_chain(qpu, "prev_qpu_hash", "qpu_row_hash")

    policy_hash = canonical_policy_hash(out / "Wilson_Ethics_Policy.json")
    zero_rows = [r for r in mw if str(r.get("p2_stage")) == "0,0"]
    zero_checked = bool(zero_rows) and all(as_bool(r.get("zero_ethics_checked")) for r in zero_rows)
    zero_policy = bool(zero_rows) and all(r.get("ethics_policy_sha256") == policy_hash for r in zero_rows)

    artifact_results = {}
    for name, expected in receipt.get("artifact_sha256", {}).items():
        p = out / name
        artifact_results[name] = p.exists() and sha256_file(p) == expected

    checks = {
        "middleware_chain_valid": ok_mw,
        "middleware_root_matches_receipt": root_mw == receipt["middleware_ledger_root_sha256"],
        "ethics_chain_valid": ok_ethics,
        "ethics_root_matches_receipt": root_ethics == receipt["ethics_ledger_root_sha256"],
        "ethics_policy_hash_matches_receipt": policy_hash == receipt["ethics_policy_sha256"],
        "every_zero_has_ethics_checkpoint": zero_checked,
        "every_zero_uses_committed_policy": zero_policy,
        "qpu_chain_valid": ok_qpu,
        "qpu_root_matches_receipt": root_qpu == receipt["qpu_evidence_ledger_root_sha256"],
        "all_receipt_artifact_hashes_match": all(artifact_results.values()) if artifact_results else True,
    }
    print(json.dumps({
        "checks": checks,
        "middleware_root": root_mw,
        "ethics_root": root_ethics,
        "ethics_policy_sha256": policy_hash,
        "zero_checkpoint_rows": len(zero_rows),
        "qpu_root": root_qpu,
        "artifact_checks": artifact_results,
    }, indent=2))
    raise SystemExit(0 if all(checks.values()) else 2)


if __name__ == "__main__":
    main()
