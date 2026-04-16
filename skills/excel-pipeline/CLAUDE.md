---
type: artifact
scope: excel-pipeline
created: 2026-04-16
updated: 2026-04-16
---

# Excel Pipeline

> Parse multi-source data → JSONL → formatted Excel.
> Install: `npx skills add duylamle/product-collection@excel-pipeline -y`

## How to use

Say **"parse data"**, **"export excel"**, or **"data pipeline"** in Claude Code.

### Typical flow:

1. **Parse** — point to source file (Excel, CSV, markdown) → skill creates JSONL
2. **Merge** — combine multiple JSONL files if needed
3. **Audit** — validate data quality, get issues report
4. **Export** — JSONL → formatted Excel with formulas, lookups, highlighting

> Each step works independently. You can export without auditing, or audit without exporting.

## Structure

```
excel-pipeline/
├── SKILL.md              ← Skill definition (start here)
├── CLAUDE.md             ← This file
├── guide/
│   └── workflow.md       ← Full workflow guide with examples
├── scripts/
│   ├── parse-excel-flat.py      ← Excel flat table → JSONL
│   ├── parse-excel-matrix.py    ← Excel matrix layout → JSONL
│   ├── parse-markdown-table.py  ← Markdown tables → JSONL
│   ├── merge.py                 ← Merge JSONL files
│   ├── audit.py                 ← Validate data quality
│   ├── diff.py                  ← Compare two JSONL versions
│   └── build-excel.py           ← JSONL → formatted Excel
└── examples/
    └── payment-channels/        ← Real-world example (13 PSPs, 1453 records)
```

## Key files to read

| When you need... | Read |
|---|---|
| How the skill works | `SKILL.md` |
| Full workflow with examples | `guide/workflow.md` |
| Script usage & arguments | `SKILL.md` → Scripts section |
| Formula registry format | `SKILL.md` → Formula Registry section |
| Real-world example | `examples/payment-channels/` |

## Build commands

```bash
pip install openpyxl    # only dependency
```
