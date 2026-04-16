---
type: artifact
scope: guide
created: 2026-04-16
updated: 2026-04-16
---

# Excel Pipeline — Full Workflow Guide

This guide walks through the complete pipeline: **Source → JSONL → Excel**.

---

## Overview

```
1. Parse     Source files → JSONL (one record per line)
2. Merge     Multiple JSONL files → single file (with dedup)
3. Audit     Validate data quality → issues.json
4. Export    JSONL → formatted Excel (.xlsx)
```

Each step is independent. You can run any step alone or chain them together.

---

## Step 1: Parse Source → JSONL

### Excel (flat table)

Most common case: Excel with headers in row 1, data below.

```bash
python scripts/parse-excel-flat.py sales.xlsx sales.jsonl
```

**With custom mapping** (rename columns, skip rows, transform types):

Create `mapping.json`:
```json
{
  "columns": {
    "Product Name": "product",
    "Unit Price": "price",
    "Qty Sold": "quantity"
  },
  "skip_rows": 0,
  "transforms": {
    "price": "float",
    "quantity": "int"
  }
}
```

```bash
python scripts/parse-excel-flat.py sales.xlsx sales.jsonl --mapping mapping.json
```

### Excel (matrix layout)

When data is organized as a matrix (columns = entities, rows = attributes):

```
           | Product A | Product B | Product C
Price      |   10.00   |   15.00   |   12.00
Stock      |   100     |   50      |   200
Category   |   Food    |   Drink   |   Food
```

```bash
python scripts/parse-excel-matrix.py products.xlsx products.jsonl --entity-field "product"
```

Output:
```jsonl
{"product": "Product A", "price": 10.0, "stock": 100, "category": "Food"}
{"product": "Product B", "price": 15.0, "stock": 50, "category": "Drink"}
```

### Markdown tables

From documentation, web pages, or notes:

```bash
python scripts/parse-markdown-table.py docs.md data.jsonl
```

Finds all markdown tables in the file and extracts them. Numeric values are auto-converted.

### Custom source?

If none of the built-in parsers fit, AI writes a custom parser for your specific format. Custom parsers are saved in your project folder, not in the skill.

---

## Step 2: Merge JSONL Files

Combine data from multiple sources:

```bash
python scripts/merge.py source1.jsonl source2.jsonl source3.jsonl -o merged.jsonl
```

**With deduplication** (by key fields):

```bash
python scripts/merge.py coda.jsonl razer.jsonl payermax.jsonl -o all.jsonl --dedup-key "market_code,payment_channel"
```

---

## Step 3: Audit Data Quality

Run automated validation:

```bash
python scripts/audit.py merged.jsonl --output issues.json
```

**With custom rules:**

Create `rules.json`:
```json
{
  "required_fields": ["product", "price", "category"],
  "numeric_fields": ["price", "stock", "min", "max"],
  "unique_key": ["product", "region"],
  "cross_checks": [
    {"rule": "min_lte_max", "min_field": "min", "max_field": "max"}
  ]
}
```

```bash
python scripts/audit.py merged.jsonl --output issues.json --rules rules.json
```

**What it checks:**
- Required fields with null/empty values
- Mixed types in a column (string + number)
- Non-numeric values in numeric fields
- Duplicate records by key
- Cross-field logic (min > max)
- High null rate (>50%) as warnings

---

## Step 4: Export to Excel

### Basic export

```bash
python scripts/build-excel.py data.jsonl --output report.xlsx
```

### With issues from audit

```bash
python scripts/build-excel.py data.jsonl --output report.xlsx --issues issues.json
```

### With formulas

Create `formula-registry.json`:
```json
[
  {
    "sheet": "Data",
    "column": "Total",
    "type": "calculated",
    "formula": "={col:price}*{col:quantity}"
  },
  {
    "sheet": "Data",
    "column": "Category Name",
    "type": "vlookup",
    "formula": "=VLOOKUP({col:category_code},Lookup_category_code!$A:$B,2,FALSE)"
  }
]
```

**Formula placeholders:**
- `{A}`, `{B}` — column letter + current row (A2, B3...)
- `{row}` — current row number
- `{col:field_name}` — column letter of that JSONL field

```bash
python scripts/build-excel.py data.jsonl --output report.xlsx --formulas formula-registry.json
```

### With conditional highlighting

Create `highlight-rules.json`:
```json
[
  {
    "condition": "field_null",
    "fields": ["price", "category"],
    "color": "FFF2CC",
    "note": "Pending data — needs confirmation"
  },
  {
    "condition": "field_value",
    "field": "status",
    "values": ["error", "failed"],
    "color": "FFB3B3",
    "note": "Error records"
  }
]
```

**Colors:** `FFF2CC` = yellow, `FFB3B3` = red, `D9EAD3` = green.

```bash
python scripts/build-excel.py data.jsonl --output report.xlsx --highlights highlight-rules.json
```

### With data sources

Create `sources.json`:
```json
[
  {"source": "Coda Docs", "url": "https://...", "notes": "Price limits by market"},
  {"source": "Internal Excel", "url": "shared-drive/file.xlsx", "notes": "Official rates"}
]
```

```bash
python scripts/build-excel.py data.jsonl --output report.xlsx --sources sources.json
```

### Full command (all options)

```bash
python scripts/build-excel.py data.jsonl \
  --output report.xlsx \
  --formulas formula-registry.json \
  --issues issues.json \
  --highlights highlight-rules.json \
  --sources sources.json
```

---

## Step 5 (optional): Diff Two Versions

When source data updates, compare old and new:

```bash
python scripts/diff.py old-data.jsonl new-data.jsonl --key "product,region" --output changelog.json
```

Output shows: records added, removed, modified (with field-level changes), and unchanged count.

---

## Tips

- **View JSONL without converting**: Install VS Code extension [Data Preview](https://marketplace.visualstudio.com/items?itemName=RandomFractalsInc.vscode-data-preview)
- **Schema evolution**: When fields change (rename, add, drop), re-run the pipeline. JSONL makes this trivial — just update the mapping and re-parse.
- **Custom parsers**: For complex sources (matrix layouts, nested tables, HTML), AI writes a project-specific parser. These live in your project folder, not in the skill.
- **Iterative workflow**: Parse → audit → fix source → re-parse → audit again. Each cycle improves data quality.
