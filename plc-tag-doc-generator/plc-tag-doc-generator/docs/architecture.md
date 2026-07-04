# Architecture — PLC Tag Documentation Generator

## Overview

Studio 5000 lets you export a controller, program, or the whole project
as an **L5X** file — plain XML. This tool parses that XML and turns it
into browsable, searchable, shareable documentation, eliminating hours
of manual tag-list transcription.

```
  L5X file (XML)
        │
        ▼
┌─────────────────────┐
│   l5x_parser.py       │   ET.parse() -> ParsedProgram
│  (stdlib XML parsing) │   (tags, data types, routines)
└─────────────────────┘
        │
        ▼
┌─────────────────────┐        ┌──────────────────────────┐
│   GUI (src/gui/)      │───────▶│  exporters.py              │
│  Tags / DataTypes /   │        │  CSV, HTML (stdlib)         │
│  Routines tables       │        │  Excel (openpyxl, optional) │
└─────────────────────┘        │  Word (python-docx, optional)│
                                 └──────────────────────────┘
```

## Components

### 1. Parser (`src/l5x_parser.py`)
Uses `xml.etree.ElementTree` (standard library, no dependencies) to
walk the L5X structure:

- `Controller/Tags/Tag` → controller-scoped tags (name, data type, tag
  type, external access, description).
- `Controller/DataTypes/DataType` → user-defined types (UDTs), each
  with its `Members`.
- `Controller/Programs/Program/Routines/Routine` → routine metadata
  (name, type — RLL/ST/FBD — and description).

This intentionally does **not** parse ladder rung logic itself (RLL
XML content), only the metadata useful for documentation. Parsing full
rung logic would require handling every instruction type and is out of
scope for a documentation tool.

### 2. Exporters (`src/exporters.py`)
- `export_csv` / `export_html`: always available, stdlib only.
- `export_excel`: requires `openpyxl`; raises `ExportDependencyError`
  with install instructions if missing, so the GUI can show a friendly
  warning instead of crashing.
- `export_word`: requires `python-docx`, same graceful-failure pattern.

### 3. GUI (`src/gui/`)
- `table_tab.py`: generic filterable, sortable table (used for Tags
  and Routines).
- `datatypes_tab.py`: tree view showing each UDT with its members
  nested underneath.
- `app.py`: main window — file loading, table population, and the
  export toolbar.

## Suggested extensions
- Parse `AddOnInstructionDefinitions` for documenting custom AOIs.
- Diff two L5X exports to produce a "what changed" report between
  program revisions — very useful for change control / audits.
- Batch mode: point the tool at a folder of L5X files and generate
  documentation for all of them in one run.
- Cross-reference tags against routines that use them (requires
  parsing rung logic, a larger undertaking).
