---
name: excel-pipeline
description: >
  Parse multi-source data (Excel, CSV, markdown) into JSONL, then export to
  formatted Excel with formulas, lookups, and conditional highlighting.
  Full pipeline: parse → merge → audit → diff → export.
  Trigger: "parse data", "import data", "export excel", "data pipeline",
  "jsonl to excel", "build excel", "audit data", "merge data".
created: 2026-04-16
updated: 2026-04-16
---

# Excel Pipeline

> Source data (Excel, CSV, markdown) → JSONL → formatted Excel.
> One skill for the full data pipeline — parse, clean, validate, export.

---

## Why JSONL as Intermediate Format?

| | Direct Excel-to-Excel | JSONL Pipeline |
|---|---|---|
| **AI-friendly** | Binary format, hard to inspect | Plain text, 1 record per line — AI reads/writes natively |
| **Multi-source merge** | Manual copy-paste | Parse each source → merge programmatically |
| **Schema evolution** | Rename columns by hand | Rename fields in script, re-export |
| **Audit trail** | No built-in validation | Automated: null checks, duplicates, type mismatches |
| **Version diff** | Compare spreadsheets manually | `diff` script shows added/removed/changed records |
| **Reproducible** | One-off manual work | Re-run pipeline anytime with updated source |

**JSONL = JSON Lines** — one JSON object per line, UTF-8. No arrays, no indentation.
```
{"name": "Alice", "score": 95}
{"name": "Bob", "score": 87}
```

**View JSONL in VS Code:** Install [Data Preview](https://marketplace.visualstudio.com/items?itemName=RandomFractalsInc.vscode-data-preview) extension — filter, search, pivot, chart, export. No need to convert to Excel just to browse.

---

## Modes

### 1. `parse` — Source → JSONL

Parse input file into JSONL. AI shows schema/structure first, proposes field mapping, waits for confirmation before running.

**Built-in parsers:**
- `parse-excel-flat.py` — Excel with flat table (1 row = 1 record)
- `parse-excel-matrix.py` — Excel matrix layout (columns = entities, rows = attributes)
- `parse-markdown-table.py` — Markdown tables (from docs, web pages)

If no parser fits the source → AI writes a custom parser, saved in your project folder (not the skill folder).

### 2. `merge` — Combine JSONL files

Merge multiple JSONL files into one. Optional deduplication by key fields.

### 3. `audit` — Validate data quality

Run after merge or on demand:
- Null/empty required fields
- Duplicate records
- Type mismatches (string in numeric field)
- Cross-field logic (min > max)
- High null-rate warnings

Output: `issues.json` + console report.

### 4. `diff` — Compare two versions

Compare old vs new JSONL → changelog:
- Records added/removed
- Field values changed
- Schema changes (new/dropped columns)

### 5. `export` — JSONL → Excel

Build formatted `.xlsx` from JSONL with:
- **Auto-detect lookup sheets** (fields ending `_code`, `_method`, `_partner` with <200 unique values)
- **Formula registry** (VLOOKUP, calculated columns) — optional JSON config
- **Conditional highlighting** (yellow = pending, red = error) — optional JSON config
- **Issues sheet** (from audit output)
- **Sources sheet** (data provenance)
- Header formatting, auto-filter, freeze panes, auto-width

---

## Prerequisites

- **Python 3.8+**
- **openpyxl**: `pip install openpyxl`

---

## Scripts

```bash
# Parse Excel (flat table)
python scripts/parse-excel-flat.py <input.xlsx> <output.jsonl> [--sheet "Sheet1"] [--mapping mapping.json]

# Parse Excel (matrix layout)
python scripts/parse-excel-matrix.py <input.xlsx> <output.jsonl> [--sheet "VN"]

# Parse markdown tables
python scripts/parse-markdown-table.py <input.md> <output.jsonl>

# Merge JSONL files
python scripts/merge.py <file1.jsonl> <file2.jsonl> -o <merged.jsonl> [--dedup-key "field1,field2"]

# Audit data quality
python scripts/audit.py <data.jsonl> [--output issues.json] [--rules rules.json]

# Diff two versions
python scripts/diff.py <old.jsonl> <new.jsonl> [--key "field1,field2"] [--output changelog.json]

# Export to Excel
python scripts/build-excel.py <data.jsonl> [--output out.xlsx] [--formulas formula-registry.json] [--issues issues.json] [--highlights highlight-rules.json] [--sources sources.json]
```

---

## Formula Registry

Optional `formula-registry.json` next to your JSONL:

```json
[
  {
    "sheet": "Data",
    "column": "Market Name",
    "type": "vlookup",
    "formula": "=VLOOKUP({B},Markets!$A:$B,2,FALSE)"
  },
  {
    "sheet": "Data",
    "column": "Price Range",
    "type": "calculated",
    "formula": "={H}-{G}"
  }
]
```

**Placeholders:** `{B}` → cell ref (B2, B3...), `{row}` → row number, `{col:field_name}` → column letter of that field.

## Highlight Rules

Optional `highlight-rules.json` — apply conditional cell highlighting to the Data sheet.

**Supported conditions:**

| Condition | What it does | Required fields |
|---|---|---|
| `field_null` | Highlight cells where value is null or empty | `fields` (array of field names) |
| `field_value` | Highlight cells matching specific values | `field` (single), `values` (array of match values) |

**Available colors:**

| Color code | Visual | Typical use |
|---|---|---|
| `FFF2CC` | Yellow | Pending data, needs confirmation |
| `FFB3B3` | Red | Errors, invalid data |
| `D9EAD3` | Green | Verified, approved |

**Example:**

```json
[
  {
    "condition": "field_null",
    "fields": ["max", "decimal", "currency"],
    "color": "FFF2CC",
    "note": "Pending — needs data from partner"
  },
  {
    "condition": "field_value",
    "field": "status",
    "values": ["error", "failed"],
    "color": "FFB3B3",
    "note": "Error records to investigate"
  },
  {
    "condition": "field_value",
    "field": "status",
    "values": ["verified"],
    "color": "D9EAD3",
    "note": "Confirmed by team"
  }
]
```

**Extending:** To add new conditions or colors, modify `build-excel.py` — the `COLOR_MAP` dict maps hex codes to openpyxl fills, and the highlight loop processes each rule type.

---

## Constraints

- **Generic** — no hardcoded domain (payment, product, etc.). Schema defined per project.
- **JSONL format** — 1 JSON object per line. No indent. UTF-8.
- **Confirm before parse** — show source structure + proposed mapping, wait for user confirmation.
- **Issues don't block** — log issues, continue pipeline. User reviews issues separately.
- **Custom parsers per project** — complex source? Write a new parser in your project folder, not in this skill.
- **Read-only JSONL for export** — Excel formulas do calculations, never modify JSONL.

---

## Works Well With

| Skill type | Why |
|---|---|
| **Data analysis / SQL** | Analyze JSONL data, write queries, validate results |
| **Documentation** | Generate data dictionaries, schema docs from JSONL |
| **Reporting** | Feed Excel output into dashboards or stakeholder reports |

Find complementary skills on [skills.sh](https://skills.sh).
