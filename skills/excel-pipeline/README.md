---
type: artifact
scope: excel-pipeline
created: 2026-04-16
updated: 2026-04-16
---

# Excel Pipeline

**Parse multi-source data into JSONL, then export to formatted Excel — with formulas, lookups, and validation.**

[![Version](https://img.shields.io/badge/version-v1.0.0-orange)](CHANGELOG.md)
[![skills.sh](https://img.shields.io/badge/skills.sh-compatible-brightgreen)](https://skills.sh/duylamle/product-collection/excel-pipeline)
[![Made with Claude Code](https://img.shields.io/badge/Made_with-Claude_Code-blueviolet?logo=anthropic)](https://claude.ai/claude-code)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/duylamle/product-collection)](https://github.com/duylamle/product-collection)

---

## The Problem

You have data in Excel files, CSV exports, markdown tables from docs — and you need to combine them into one clean spreadsheet. Today that means:

- Copy-paste between files (error-prone, no audit trail)
- Manual column renaming and reformatting
- No way to validate data quality automatically
- Redo everything when source data updates

## The Solution

This skill gives AI a **reproducible pipeline**: parse any source into JSONL (a simple text format AI reads natively), then export to a formatted Excel with formulas, lookups, and conditional highlighting.

```
Source Files          JSONL              Excel
┌──────────┐    ┌──────────────┐    ┌──────────────┐
│ Excel    │───→│              │    │ Data sheet   │
│ CSV      │───→│  Merge +     │───→│ Lookup sheets│
│ Markdown │───→│  Audit       │    │ Issues sheet │
│ Web docs │───→│              │    │ Formulas     │
└──────────┘    └──────────────┘    └──────────────┘
```

**Why JSONL in the middle?** It's plain text (AI reads it natively), one record per line (easy to merge), and changes are trackable (diff two versions to see what changed).

## Install

```bash
npx skills add duylamle/product-collection@excel-pipeline -y
```

## Quick Start

1. Install the skill (above)
2. In Claude Code, say: **"Parse this Excel file into JSONL"** or **"Export this data to Excel"**
3. AI reads your source, shows the schema, proposes field mapping
4. You confirm → AI runs the pipeline
5. Get a formatted `.xlsx` with auto-filter, freeze panes, and optional formulas

## Prerequisites

- **Python 3.8+**
- **openpyxl**: `pip install openpyxl`

## What's Inside

```
excel-pipeline/
├── SKILL.md                         ← Skill definition (Claude reads this)
├── CLAUDE.md                        ← Project map for Claude
├── guide/
│   └── workflow.md                  ← Full workflow guide with examples
├── scripts/
│   ├── parse-excel-flat.py          ← Excel flat table → JSONL
│   ├── parse-excel-matrix.py        ← Excel matrix layout → JSONL
│   ├── parse-markdown-table.py      ← Markdown tables → JSONL
│   ├── merge.py                     ← Merge JSONL files + dedup
│   ├── audit.py                     ← Validate data quality
│   ├── diff.py                      ← Compare two JSONL versions
│   └── build-excel.py               ← JSONL → formatted Excel
└── examples/
    └── (see guide for real-world example)
```

## Pipeline Modes

| Mode | What it does |
|---|---|
| **Parse** | Source file → JSONL. Built-in parsers for Excel (flat + matrix), CSV, markdown tables |
| **Merge** | Combine multiple JSONL files, optional dedup by key fields |
| **Audit** | Validate: nulls, duplicates, type mismatches, cross-field logic (e.g., min > max) |
| **Diff** | Compare old vs new JSONL → changelog (added/removed/modified records) |
| **Export** | JSONL → Excel with formulas, lookup sheets, conditional highlighting, issues sheet |

## Excel Export Features

- **Auto-detect lookup sheets** — fields ending `_code`, `_method`, `_partner` with <200 unique values
- **Formula registry** — define Excel formulas (VLOOKUP, calculated columns, and more) in a JSON config
- **Conditional highlighting** — highlight cells by rules (null fields, specific values) with 3 colors (yellow/red/green, extensible)
- **Issues sheet** — from audit output, color-coded by priority
- **Sources sheet** — track data provenance
- **Professional formatting** — dark blue headers, auto-filter, freeze panes, auto-width

## Guides

| Guide | When to read |
|---|---|
| [Full Workflow](guide/workflow.md) | Understanding the complete pipeline with examples |

## Works Well With

| Skill type | Why |
|---|---|
| Data analysis | Analyze JSONL data, write queries, validate results |
| Documentation | Generate data dictionaries from JSONL schema |
| Reporting | Feed Excel output into dashboards |
| [Data Preview](https://marketplace.visualstudio.com/items?itemName=RandomFractalsInc.vscode-data-preview) (VS Code) | View JSONL as spreadsheet — filter, search, pivot, chart, export |
| [jsongrid.com](https://jsongrid.com/json-grid) (Browser) | Paste or upload JSONL, view as interactive grid — no install needed |

Find complementary skills on [skills.sh](https://skills.sh).

---

<p align="center">
  Thanks for visiting <b>Excel Pipeline</b>
  <br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=duylamle.product-collection.excel-pipeline&style=flat" alt="visitors"/>
</p>

## License

[MIT](../../LICENSE)
