"""
Compare two JSONL files, output changelog.
Usage: python diff.py <old.jsonl> <new.jsonl> [--key "field1,field2"] [--output changelog.json]
"""
import json, sys, argparse

def load_jsonl(path):
    records = {}
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                records[i] = json.loads(line)
    return records

def make_key(rec, key_fields):
    return tuple(str(rec.get(k, "")) for k in key_fields)

def diff(old_path, new_path, key_fields_str=None, output_path=None):
    old_recs = load_jsonl(old_path)
    new_recs = load_jsonl(new_path)

    if not key_fields_str:
        # Auto-detect: use all fields of first record
        sample = list(old_recs.values())[0] if old_recs else list(new_recs.values())[0]
        key_fields = list(sample.keys())
        print(f"Auto key: all fields ({len(key_fields)} fields)")
    else:
        key_fields = [k.strip() for k in key_fields_str.split(",")]

    old_by_key = {make_key(r, key_fields): r for r in old_recs.values()}
    new_by_key = {make_key(r, key_fields): r for r in new_recs.values()}

    old_keys = set(old_by_key.keys())
    new_keys = set(new_by_key.keys())

    added = new_keys - old_keys
    removed = old_keys - new_keys
    common = old_keys & new_keys

    changes = []
    for key in common:
        old_r = old_by_key[key]
        new_r = new_by_key[key]
        diffs = {}
        all_fields = set(list(old_r.keys()) + list(new_r.keys()))
        for f in all_fields:
            ov = old_r.get(f)
            nv = new_r.get(f)
            if ov != nv:
                diffs[f] = {"old": ov, "new": nv}
        if diffs:
            changes.append({"key": dict(zip(key_fields, key)), "changes": diffs})

    changelog = {
        "summary": {
            "old_records": len(old_recs),
            "new_records": len(new_recs),
            "added": len(added),
            "removed": len(removed),
            "modified": len(changes),
            "unchanged": len(common) - len(changes),
        },
        "added": [dict(zip(key_fields, k)) for k in sorted(added)],
        "removed": [dict(zip(key_fields, k)) for k in sorted(removed)],
        "modified": changes,
    }

    print(f"=== Diff Report ===")
    print(f"Old: {len(old_recs)} records")
    print(f"New: {len(new_recs)} records")
    print(f"Added: {len(added)}")
    print(f"Removed: {len(removed)}")
    print(f"Modified: {len(changes)}")
    print(f"Unchanged: {len(common) - len(changes)}")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(changelog, f, ensure_ascii=False, indent=2, default=str)
        print(f"\nChangelog saved: {output_path}")

    return changelog

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Diff two JSONL files")
    parser.add_argument("old", help="Old JSONL file")
    parser.add_argument("new", help="New JSONL file")
    parser.add_argument("--key", help="Comma-separated key fields")
    parser.add_argument("--output", "-o", help="Output changelog JSON")
    args = parser.parse_args()
    diff(args.old, args.new, args.key, args.output)
