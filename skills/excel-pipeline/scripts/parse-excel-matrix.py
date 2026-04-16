"""
Parse Excel matrix layout (columns = entities, rows = attributes) → JSONL.
Usage: python parse-excel-matrix.py <input.xlsx> <output.jsonl> [--sheet "Sheet1"] [--entity-field "market"]

Matrix layout example:
           | Entity A | Entity B | Entity C
Attribute1 |   val    |   val    |   val
Attribute2 |   val    |   val    |   val

Output: one JSONL record per entity with all attributes as fields.
"""
import openpyxl, json, sys, argparse

def parse(input_path, output_path, sheet_name=None, entity_field="entity"):
    wb = openpyxl.load_workbook(input_path, read_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active

    rows = list(ws.iter_rows(values_only=True))
    if not rows or len(rows) < 2:
        print("Empty or insufficient data")
        return

    # First row: entity names (skip first cell which is the attribute label column)
    header = rows[0]
    entities = []
    for i, cell in enumerate(header):
        if i == 0:
            continue
        if cell and str(cell).strip():
            entities.append((i, str(cell).strip()))

    if not entities:
        print("No entities found in header row")
        return

    # Build records: one per entity
    records = {name: {entity_field: name} for _, name in entities}

    # Each subsequent row: attribute name in col 0, values in entity columns
    for row in rows[1:]:
        attr_name = row[0] if row[0] else None
        if not attr_name:
            continue
        attr_name = str(attr_name).strip()
        # snake_case the attribute name
        import re
        attr_key = re.sub(r'[^\w\s]', '', attr_name)
        attr_key = re.sub(r'\s+', '_', attr_key.strip()).lower()

        for col_idx, entity_name in entities:
            val = row[col_idx] if col_idx < len(row) else None
            records[entity_name][attr_key] = val

    # Write JSONL
    result = list(records.values())
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in result:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")

    print(f"Parsed {len(result)} entities, {len(rows)-1} attributes")
    print(f"Entities: {[name for _, name in entities]}")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse matrix Excel → JSONL")
    parser.add_argument("input", help="Input Excel file")
    parser.add_argument("output", help="Output JSONL file")
    parser.add_argument("--sheet", help="Sheet name (default: active sheet)")
    parser.add_argument("--entity-field", default="entity", help="Field name for entity column (default: entity)")
    args = parser.parse_args()
    parse(args.input, args.output, args.sheet, args.entity_field)
