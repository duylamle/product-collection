"""
Parse Excel flat table (1 row = 1 record) → JSONL.
Usage: python parse-excel-flat.py <input.xlsx> <output.jsonl> [--sheet "Sheet1"] [--mapping mapping.json]

Mapping JSON format:
{
  "columns": {"Excel Column Name": "jsonl_field_name", ...},
  "skip_rows": 0,
  "transforms": {"field": "transform_type"}  // optional: "float", "int", "str", "lower"
}

If no mapping provided, uses Excel header row as field names (snake_case).
"""
import openpyxl, json, sys, re, argparse

def to_snake_case(s):
    s = re.sub(r'[^\w\s]', '', str(s))
    s = re.sub(r'\s+', '_', s.strip())
    return s.lower()

def apply_transform(val, transform):
    if val is None:
        return None
    try:
        if transform == "float":
            return float(val)
        elif transform == "int":
            return int(val)
        elif transform == "str":
            return str(val)
        elif transform == "lower":
            return str(val).lower()
    except (ValueError, TypeError):
        return val
    return val

def parse(input_path, output_path, sheet_name=None, mapping_path=None):
    wb = openpyxl.load_workbook(input_path, read_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        print("Empty sheet")
        return

    # Load mapping
    col_map = None
    skip_rows = 0
    transforms = {}
    if mapping_path:
        with open(mapping_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
        col_map = mapping.get("columns", {})
        skip_rows = mapping.get("skip_rows", 0)
        transforms = mapping.get("transforms", {})

    # Find header row
    header_row = rows[skip_rows]
    if col_map:
        # Map Excel column names to JSONL field names
        field_map = {}  # col_index -> jsonl_field
        for idx, cell in enumerate(header_row):
            if cell and str(cell).strip() in col_map:
                field_map[idx] = col_map[str(cell).strip()]
    else:
        # Auto: snake_case header names
        field_map = {}
        for idx, cell in enumerate(header_row):
            if cell:
                field_map[idx] = to_snake_case(cell)

    # Parse data rows
    records = []
    for row in rows[skip_rows + 1:]:
        record = {}
        has_data = False
        for idx, field in field_map.items():
            val = row[idx] if idx < len(row) else None
            if val is not None:
                has_data = True
            if field in transforms:
                val = apply_transform(val, transforms[field])
            record[field] = val
        if has_data:
            records.append(record)

    # Write JSONL
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")

    print(f"Parsed {len(records)} records, {len(field_map)} fields")
    print(f"Fields: {list(field_map.values())}")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse flat Excel → JSONL")
    parser.add_argument("input", help="Input Excel file")
    parser.add_argument("output", help="Output JSONL file")
    parser.add_argument("--sheet", help="Sheet name (default: active sheet)")
    parser.add_argument("--mapping", help="Mapping JSON file")
    args = parser.parse_args()
    parse(args.input, args.output, args.sheet, args.mapping)
