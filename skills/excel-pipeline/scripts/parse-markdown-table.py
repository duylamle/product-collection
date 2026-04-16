"""
Parse markdown tables → JSONL.
Usage: python parse-markdown-table.py <input.md> <output.jsonl>

Finds all markdown tables in the file and extracts rows as JSONL records.
Handles standard markdown table syntax:
  | Header1 | Header2 |
  |---------|---------|
  | val1    | val2    |
"""
import json, sys, re, argparse

def parse_markdown_tables(text):
    """Extract all markdown tables from text, return list of record lists."""
    lines = text.split("\n")
    tables = []
    current_table = []
    in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            current_table.append(stripped)
            in_table = True
        else:
            if in_table and current_table:
                tables.append(current_table)
                current_table = []
            in_table = False

    if current_table:
        tables.append(current_table)

    all_records = []
    for table_lines in tables:
        if len(table_lines) < 3:  # header + separator + at least 1 data row
            continue

        # Parse header
        header = [cell.strip() for cell in table_lines[0].split("|")[1:-1]]

        # Skip separator line (line with dashes)
        # Find first non-separator line after header
        data_start = 1
        for i in range(1, len(table_lines)):
            if re.match(r'^\|[\s\-:]+\|$', table_lines[i].replace("|", "|").strip()):
                data_start = i + 1
                break

        # Parse data rows
        for line in table_lines[data_start:]:
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            if len(cells) == len(header):
                record = {}
                for h, v in zip(header, cells):
                    # snake_case header
                    key = re.sub(r'[^\w\s]', '', h)
                    key = re.sub(r'\s+', '_', key.strip()).lower()
                    # Try numeric conversion
                    if v and re.match(r'^-?\d+\.?\d*$', v.replace(",", "")):
                        try:
                            v = float(v.replace(",", ""))
                            if v == int(v):
                                v = int(v)
                        except ValueError:
                            pass
                    elif v == "" or v == "-":
                        v = None
                    record[key] = v
                all_records.append(record)

    return all_records

def parse(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    records = parse_markdown_tables(text)

    if not records:
        print("No markdown tables found")
        return

    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")

    # Detect fields
    fields = []
    seen = set()
    for rec in records:
        for k in rec:
            if k not in seen:
                fields.append(k)
                seen.add(k)

    print(f"Parsed {len(records)} records from markdown tables")
    print(f"Fields: {fields}")
    print(f"Output: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse markdown tables → JSONL")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("output", help="Output JSONL file")
    args = parser.parse_args()
    parse(args.input, args.output)
