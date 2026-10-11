# PLC Tag Documentation Generator

A **Python + Tkinter** desktop tool that parses Rockwell Automation /
Allen-Bradley **L5X** files (the XML export from Studio 5000) and
automatically generates browsable, exportable documentation of all
Tags, User-Defined Data Types, and Routines — saving hours of manual
documentation work.

Designed to run **directly in Thonny IDE** and also from the command line.

![status](https://img.shields.io/badge/status-functional-brightgreen)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

## Features

- **Open any L5X export** (controller, program, or full project export
  from Studio 5000, File > Save As > L5X or right-click > Export).
- **Browse Tags** in a filterable, sortable table (name, tag type, data
  type, external access, description).
- **Browse User-Defined Data Types (UDTs)** as an expandable tree with
  members nested underneath.
- **Browse Routines** grouped by program, with type (RLL/ST/FBD) and
  description.
- **One-click export** to:
  - CSV (always available, no dependencies)
  - HTML (styled, shareable single-page report, no dependencies)
  - Excel `.xlsx` (requires `openpyxl`)
  - Word `.docx` (requires `python-docx`)
- **Sample L5X file included** (`sample_data/sample_program.L5X`) so
  you can try the tool immediately without needing a real export.
- **No required dependencies**: parsing, CSV, and HTML export all work
  with just Python's standard library.

## Repository structure

```
plc-tag-doc-generator/
├── main.py                       # Entry point (run this file)
├── requirements.txt               # Optional: openpyxl, python-docx
├── sample_data/
│   └── sample_program.L5X         # Synthetic sample L5X for demo/testing
├── src/
│   ├── l5x_parser.py              # XML parsing of L5X files (stdlib only)
│   ├── exporters.py               # CSV / HTML / Excel / Word export
│   └── gui/
│       ├── app.py                  # Main window and export toolbar
│       ├── table_tab.py            # Reusable filterable/sortable table
│       └── datatypes_tab.py        # Tree view for UDTs and their members
├── data/                          # Exported documentation is written here
└── docs/
    └── architecture.md            # Architecture details
```

## How to run in Thonny IDE

1. Download or clone this repository.
2. Open **Thonny**.
3. `File > Open...` and select `main.py`.
4. Press **F5** (or the ▶ Run button).
5. Click **"Load Sample File"** to see it working immediately, or
   **"Open L5X File..."** to load your own Studio 5000 export.

> **Note on Excel/Word export**: if you click "Export Excel" or "Export
> Word" and see a missing-dependency warning, install the needed
> package from Thonny: `Tools > Manage packages > search "openpyxl"`
> (or `"python-docx"`) `> Install`.

## How to run from the command line

```bash
git clone https://github.com/your-username/plc-tag-doc-generator.git
cd plc-tag-doc-generator
pip install -r requirements.txt   # optional, only for Excel/Word export
python main.py
```

## How to export your own project's documentation

1. In Studio 5000: right-click the controller (or a program) in the
   project tree → **Export** → save as `.L5X`.
2. In this app: **Open L5X File...** and select the exported file.
3. Use the **Export** buttons to generate CSV, HTML, Excel, or Word
   documentation in the `data/` folder.

## Roadmap / suggested extensions

- Parse Add-On Instruction (AOI) definitions.
- Diff two L5X exports to generate a "what changed" report between
  revisions, useful for change-control audits.
- Batch-process a folder of L5X files in one run.
- Cross-reference which routines use each tag (requires parsing rung
  logic, not just metadata).

## License

MIT — see [LICENSE](LICENSE).
* **Liability & Safety Disclaimer:** This software and its documentation are provided "as is" for educational and informational purposes only. Industrial automation involving live machinery carries inherent risks of property damage, production downtime, physical injury, or loss of life. The creators, contributors, and maintainers of this repository assume absolutely no responsibility or liability for any errors, malfunctioning, damages, or financial losses resulting from the use or misuse of this code. Any implementation on a live production floor is done completely at the user's own risk, and the final engineer or technician deploying this system is solely responsible for verifying its safety, accuracy, and compliance with local industrial regulations.*

