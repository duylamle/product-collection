---
type: artifact
scope: excel-pipeline
created: 2026-04-16
updated: 2026-04-16
---

# Changelog — excel-pipeline

## v1.0.0 (2026-04-16)

### Added
- SKILL.md — full skill definition (5 modes: parse, merge, audit, diff, export)
- CLAUDE.md — project map + quick reference
- **Scripts** (7 Python scripts):
  - `parse-excel-flat.py` — Excel flat table → JSONL (with mapping JSON support)
  - `parse-excel-matrix.py` — Excel matrix layout → JSONL
  - `parse-markdown-table.py` — Markdown tables → JSONL
  - `merge.py` — Merge multiple JSONL files with optional dedup
  - `audit.py` — Validate JSONL: nulls, duplicates, types, cross-field logic
  - `diff.py` — Compare two JSONL versions → changelog
  - `build-excel.py` — JSONL → formatted Excel with formulas, lookups, highlights
- **Guide**: `workflow.md` — full pipeline walkthrough with examples
- README.md with badges, pipeline diagram, modes table
