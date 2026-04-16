"""
Merge multiple JSONL files into one. Optional deduplication.
Usage: python merge.py <file1.jsonl> <file2.jsonl> ... -o <merged.jsonl> [--dedup-key "field1,field2"]
"""
import json, sys, argparse

def load_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def merge(input_files, output_path, dedup_key=None):
    all_records = []
    for fp in input_files:
        recs = load_jsonl(fp)
        print(f"  {fp}: {len(recs)} records")
        all_records.extend(recs)

    print(f"Total before dedup: {len(all_records)}")

    if dedup_key:
        keys = [k.strip() for k in dedup_key.split(",")]
        seen = set()
        deduped = []
        dupes = 0
        for rec in all_records:
            k = tuple(rec.get(f, "") for f in keys)
            if k not in seen:
                seen.add(k)
                deduped.append(rec)
            else:
                dupes += 1
        all_records = deduped
        print(f"Removed {dupes} duplicates (key: {keys})")

    with open(output_path, "w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")

    print(f"Output: {len(all_records)} records → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge JSONL files")
    parser.add_argument("inputs", nargs="+", help="Input JSONL files")
    parser.add_argument("-o", "--output", required=True, help="Output JSONL file")
    parser.add_argument("--dedup-key", help="Comma-separated fields for dedup")
    args = parser.parse_args()
    merge(args.inputs, args.output, args.dedup_key)
