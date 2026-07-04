"""
app.py
--------
Main application window. Lets the user open an L5X file, browse the
parsed Tags / Data Types / Routines in tables, and export the results
to CSV, HTML, Excel, or Word.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from src.l5x_parser import parse_l5x_file, L5XParseError
from src.exporters import (
    export_csv, export_html, export_excel, export_word, ExportDependencyError
)
from src.gui.table_tab import TableTab
from src.gui.datatypes_tab import DataTypesTab

APP_TITLE = "PLC Tag Documentation Generator"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data")
SAMPLE_FILE = os.path.join(PROJECT_ROOT, "sample_data", "sample_program.L5X")


class DocGenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1100x680")
        self.minsize(900, 560)

        self.parsed = None
        self.current_filepath = None

        self._build_style()
        self._build_layout()

    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

    def _build_layout(self):
        header = ttk.Frame(self, padding=(14, 10))
        header.pack(fill="x")

        ttk.Label(header, text=APP_TITLE, font=("Segoe UI", 15, "bold")).pack(side="left")

        open_btn = ttk.Button(header, text="Open L5X File...", command=self._open_file)
        open_btn.pack(side="right", padx=(6, 0))
        sample_btn = ttk.Button(header, text="Load Sample File", command=self._load_sample)
        sample_btn.pack(side="right", padx=(6, 0))

        self.file_lbl = ttk.Label(self, text="No file loaded.", foreground="#6b7280", padding=(14, 0))
        self.file_lbl.pack(fill="x")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tags_tab = TableTab(
            notebook,
            columns=("name", "tag_type", "data_type", "external_access", "description"),
            headers={
                "name": "Name", "tag_type": "Tag Type", "data_type": "Data Type",
                "external_access": "External Access", "description": "Description",
            },
            widths={"name": 200, "tag_type": 90, "data_type": 130,
                    "external_access": 130, "description": 400},
        )
        self.datatypes_tab = DataTypesTab(notebook)
        self.routines_tab = TableTab(
            notebook,
            columns=("program", "name", "type", "description"),
            headers={"program": "Program", "name": "Routine", "type": "Type", "description": "Description"},
            widths={"program": 160, "name": 200, "type": 80, "description": 480},
        )

        notebook.add(self.tags_tab, text="  Tags  ")
        notebook.add(self.datatypes_tab, text="  Data Types  ")
        notebook.add(self.routines_tab, text="  Routines  ")

        export_bar = ttk.LabelFrame(self, text="Export documentation", padding=10)
        export_bar.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Button(export_bar, text="Export CSV", command=self._export_csv).pack(side="left", padx=4)
        ttk.Button(export_bar, text="Export HTML", command=self._export_html).pack(side="left", padx=4)
        ttk.Button(export_bar, text="Export Excel (.xlsx)", command=self._export_excel).pack(side="left", padx=4)
        ttk.Button(export_bar, text="Export Word (.docx)", command=self._export_word).pack(side="left", padx=4)

        self.status_lbl = ttk.Label(export_bar, text="", foreground="#1f9d55")
        self.status_lbl.pack(side="right")

    # -- File loading ---------------------------------------------------

    def _open_file(self):
        filepath = filedialog.askopenfilename(
            title="Select an L5X file",
            filetypes=[("Rockwell L5X files", "*.L5X *.l5x"), ("All files", "*.*")],
        )
        if filepath:
            self._load_file(filepath)

    def _load_sample(self):
        if os.path.exists(SAMPLE_FILE):
            self._load_file(SAMPLE_FILE)
        else:
            messagebox.showerror("Sample file missing", f"Could not find:\n{SAMPLE_FILE}")

    def _load_file(self, filepath):
        try:
            parsed = parse_l5x_file(filepath)
        except L5XParseError as exc:
            messagebox.showerror("Could not parse file", str(exc))
            return
        except Exception as exc:
            messagebox.showerror("Unexpected error", f"Could not read file:\n{exc}")
            return

        self.parsed = parsed
        self.current_filepath = filepath
        counts = parsed.summary_counts()
        self.file_lbl.config(
            text=(f"Loaded: {os.path.basename(filepath)}  —  Controller: {parsed.controller_name}  "
                  f"—  {counts['tags']} tags, {counts['data_types']} data types, "
                  f"{counts['routines']} routines"),
            foreground="#1f2937",
        )
        self._refresh_tables()
        self.status_lbl.config(text="")

    def _refresh_tables(self):
        self.tags_tab.load_rows([
            (t["name"], t["tag_type"], t["data_type"], t["external_access"], t["description"])
            for t in self.parsed.tags
        ])
        self.datatypes_tab.load_data_types(self.parsed.data_types)
        self.routines_tab.load_rows([
            (r["program"], r["name"], r["type"], r["description"])
            for r in self.parsed.routines
        ])

    # -- Export -----------------------------------------------------------

    def _require_parsed(self):
        if not self.parsed:
            messagebox.showwarning("No file loaded", "Open an L5X file first (or load the sample file).")
            return False
        return True

    def _choose_output_dir(self):
        os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
        return DEFAULT_OUTPUT_DIR

    def _export_csv(self):
        if not self._require_parsed():
            return
        out_dir = self._choose_output_dir()
        paths = export_csv(self.parsed, out_dir)
        self.status_lbl.config(text=f"CSV exported to {out_dir}", foreground="#1f9d55")
        messagebox.showinfo("Export complete", "CSV files created:\n" + "\n".join(paths.values()))

    def _export_html(self):
        if not self._require_parsed():
            return
        out_dir = self._choose_output_dir()
        path = export_html(self.parsed, out_dir)
        self.status_lbl.config(text=f"HTML exported to {out_dir}", foreground="#1f9d55")
        messagebox.showinfo("Export complete", f"HTML documentation created:\n{path}")

    def _export_excel(self):
        if not self._require_parsed():
            return
        out_dir = self._choose_output_dir()
        try:
            path = export_excel(self.parsed, out_dir)
        except ExportDependencyError as exc:
            messagebox.showwarning("Missing dependency", str(exc))
            return
        self.status_lbl.config(text=f"Excel exported to {out_dir}", foreground="#1f9d55")
        messagebox.showinfo("Export complete", f"Excel workbook created:\n{path}")

    def _export_word(self):
        if not self._require_parsed():
            return
        out_dir = self._choose_output_dir()
        try:
            path = export_word(self.parsed, out_dir)
        except ExportDependencyError as exc:
            messagebox.showwarning("Missing dependency", str(exc))
            return
        self.status_lbl.config(text=f"Word document exported to {out_dir}", foreground="#1f9d55")
        messagebox.showinfo("Export complete", f"Word document created:\n{path}")


def run():
    app = DocGenApp()
    app.mainloop()
