"""
Audit JSONL file: null checks, duplicates, type mismatches, cross-field logic.
Usage: python audit.py <data.jsonl> [--output issues.json] [--rules rules.json]

Rules JSON format (optional):
{
  "required_fields": ["field1", "field2"],
  "numeric_fields": ["min", "max"],
  "unique_key": ["market_code", "payment_channel", "payment_partner"],
  "cross_checks": [{"rule": "min_lte_max", "min_field": "min", "max_field": "max"}]
}

If no rules provided, runs generic checks on all fields.
"""
import json, sys, argparse
from collections import Counter, defaultdict

def load_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                try:
                    records.append((i + 1, json.loads(line)))
                except json.JSONDecodeError:
                    records.append((i + 1, {"__parse_error": line[:100]}))
    return records

def audit(input_path, output_path=None, rules_path=None):
    records = load_jsonl(input_path)
    if not records:
        print("Empty file")
        return

    # Load rules
    rules = {}
    if rules_path:
        with open(rules_path, "r", encoding="utf-8") as f:
            rules = json.load(f)

    required = rules.get("required_fields", [])
    numeric = rules.get("numeric_fields", [])
    unique_key = rules.get("unique_key", [])
    cross_checks = rules.get("cross_checks", [])

    issues = []
    all_fields = set()
    field_null_count = Counter()
    field_type_count = defaultdict(Counter)

    # Collect stats
    for line_num, rec in records:
        if "__parse_error" in rec:
            issues.append({
                "priority": "High", "line": line_num,
                "field": "__parse_error", "issue": "JSON parse error",
                "detail": rec["__parse_error"], "status": "Pending",
            })
            continue

        all_fields.update(rec.keys())
        for k, v in rec.items():
            if v is None or v == "":
                field_null_count[k] += 1
            field_type_count[k][type(v).__name__] += 1

    total = len(records)

    # 1. Required field checks
    for field in required:
        nulls = field_null_count.get(field, 0)
        if nulls > 0:
            issues.append({
                "priority": "High", "line": "multiple",
                "field": field, "issue": f"Required field null/empty: {nulls}/{total}",
                "detail": f"{nulls} records missing '{field}'",
                "status": "Pending",
            })

    # 2. Type consistency
    for field, types in field_type_count.items():
        non_null_types = {t: c for t, c in types.items() if t != "NoneType"}
        if len(non_null_types) > 1:
            issues.append({
                "priority": "Medium", "line": "multiple",
                "field": field, "issue": "Mixed types",
                "detail": f"Types: {dict(non_null_types)}",
                "status": "Pending",
            })

    # 3. Numeric field checks
    for field in numeric:
        for line_num, rec in records:
            if "__parse_error" in rec:
                continue
            v = rec.get(field)
            if v is not None and v != "" and not isinstance(v, (int, float)):
                issues.append({
                    "priority": "Medium", "line": line_num,
                    "field": field, "issue": f"Non-numeric value: {v}",
                    "detail": f"Expected number, got {type(v).__name__}: {v}",
                    "status": "Pending",
                })

    # 4. Duplicate check
    if unique_key:
        seen = defaultdict(list)
        for line_num, rec in records:
            if "__parse_error" in rec:
                continue
            key = tuple(rec.get(k, "") for k in unique_key)
            seen[key].append(line_num)
        for key, lines in seen.items():
            if len(lines) > 1:
                issues.append({
                    "priority": "Medium", "line": str(lines),
                    "field": ",".join(unique_key),
                    "issue": f"Duplicate: {len(lines)} records",
                    "detail": f"Key: {dict(zip(unique_key, key))}",
                    "status": "Pending",
                })

    # 5. Cross-field checks
    for check in cross_checks:
        if check["rule"] == "min_lte_max":
            min_f = check["min_field"]
            max_f = check["max_field"]
            for line_num, rec in records:
                if "__parse_error" in rec:
                    continue
                mn = rec.get(min_f)
                mx = rec.get(max_f)
                if mn is not None and mx is not None:
                    try:
                        if float(mn) > float(mx):
                            issues.append({
                                "priority": "High", "line": line_num,
                                "field": f"{min_f},{max_f}",
                                "issue": f"min > max: {mn} > {mx}",
                                "detail": f"{min_f}={mn}, {max_f}={mx}",
                                "status": "Pending",
                            })
                    except (ValueError, TypeError):
                        pass

    # 6. Generic null report (fields with >50% null)
    for field in all_fields:
        nulls = field_null_count.get(field, 0)
        if nulls > total * 0.5 and field not in required:
            issues.append({
                "priority": "Low", "line": "multiple",
                "field": field, "issue": f"High null rate: {nulls}/{total} ({nulls*100//total}%)",
                "detail": f"Field '{field}' mostly empty",
                "status": "Note",
            })

    # Report
    print(f"=== Audit Report ===")
    print(f"Records: {total}")
    print(f"Fields: {len(all_fields)}")
    print(f"Issues: {len(issues)} (High: {sum(1 for i in issues if i['priority']=='High')}, "
          f"Medium: {sum(1 for i in issues if i['priority']=='Medium')}, "
          f"Low: {sum(1 for i in issues if i['priority']=='Low')})")

    if issues:
        print(f"\nTop issues:")
        for i in sorted(issues, key=lambda x: {"High":0,"Medium":1,"Low":2}.get(x["priority"],3))[:15]:
            print(f"  [{i['priority']}] {i['field']}: {i['issue']}")

    # Save
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(issues, f, ensure_ascii=False, indent=2)
        print(f"\nIssues saved: {output_path}")

    return issues

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit JSONL file")
    parser.add_argument("input", help="Input JSONL file")
    parser.add_argument("--output", "-o", help="Output issues JSON")
    parser.add_argument("--rules", help="Rules JSON file")
    args = parser.parse_args()
    audit(args.input, args.output, args.rules)
