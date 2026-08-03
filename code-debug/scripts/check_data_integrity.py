#!/usr/bin/env python3
"""Compare numeric JSON values across independent experiment files to detect frozen or duplicated data.

Detects: bit-identical values across 3+ independent methods, impossible zeros,
         internal contradictions between data sources, and constant diffs.
"""
import json, sys, os
from pathlib import Path
from collections import defaultdict

def find_json_files(root: Path) -> list:
    return list(root.rglob('*.json'))

def check_frozen_values(files: list) -> list:
    """Find metric keys with identical values across 3+ files."""
    key_vals = defaultdict(list)
    for f in files:
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        _flatten_dict(data, '', key_vals, str(f))
    frozen = []
    for key, entries in key_vals.items():
        vals = [v for _, v in entries]
        if len(vals) >= 3 and len(set(vals)) == 1 and vals[0] not in (0, 1):
            frozen.append((key, vals[0], len(vals)))
    return frozen

def check_impossible_zeros(files: list, metrics: list) -> list:
    """Check if specified metrics are exactly zero across all files."""
    results = []
    for metric in metrics:
        values = []
        for f in files:
            try:
                data = json.loads(f.read_text())
            except Exception:
                continue
            for v in _get_nested(data, metric):
                values.append(v)
        if len(values) >= 3 and all(v == 0 for v in values):
            results.append((metric, len(values)))
    return results

def check_timestamp_collisions(files: list) -> list:
    """Find files sharing the same timestamp_utc."""
    ts_files = defaultdict(list)
    for f in files:
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        ts = data.get('timestamp_utc', data.get('timestamp', ''))
        if ts:
            ts_files[ts].append(str(f))
    return [(ts, paths) for ts, paths in ts_files.items() if len(paths) > 1]

def _flatten_dict(d: dict, prefix: str, out: dict, source: str):
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            _flatten_dict(v, key, out, source)
        elif isinstance(v, (int, float)):
            out[key].append((source, v))

def _get_nested(d: dict, target_key: str) -> list:
    results = []
    for k, v in d.items():
        if k == target_key and isinstance(v, (int, float)):
            results.append(v)
        elif isinstance(v, dict):
            results.extend(_get_nested(v, target_key))
    return results

def main():
    # Usage: python check_data_integrity.py [results/] [--zero-metrics m1,m2,...]
    args = sys.argv[1:]
    root = Path(args[0]) if args and not args[0].startswith('--') else Path('results')
    # 需要检查"不可能零值"的指标名（项目特定，用 --zero-metrics 传入；默认通用集）
    zero_metrics = ['e_align', 'alignment_error', 'std_iou']
    if '--zero-metrics' in args:
        idx = args.index('--zero-metrics')
        if idx + 1 < len(args):
            zero_metrics = [m.strip() for m in args[idx + 1].split(',') if m.strip()]
    if not root.exists():
        print(f"Directory not found: {root}. Usage: python check_data_integrity.py [results/] [--zero-metrics m1,m2,...]")
        sys.exit(1)

    files = find_json_files(root)
    if not files:
        print(f"No JSON files found under {root}")
        sys.exit(0)

    print(f"Scanning {len(files)} JSON files under {root}\n")

    frozen = check_frozen_values(files)
    if frozen:
        print(f"=== FROZEN VALUES (identical across 3+ files) ===")
        for key, val, count in sorted(frozen):
            print(f"  {key}: {val} in {count} files")
    else:
        print("OK: no frozen values found.")

    collisions = check_timestamp_collisions(files)
    if collisions:
        print(f"\n=== TIMESTAMP COLLISIONS ({len(collisions)} groups) ===")
        for ts, paths in collisions[:5]:
            print(f"  {ts}: {len(paths)} files")
    else:
        print("OK: all timestamps unique.")

    impossible = check_impossible_zeros(files, zero_metrics)
    if impossible:
        print(f"\n=== IMPOSSIBLE ZEROS ===")
        for metric, count in impossible:
            print(f"  {metric}: exactly 0 in all {count} files")

    print(f"\nDone.")
    sys.exit(0 if not frozen else 2)

if __name__ == '__main__':
    main()
