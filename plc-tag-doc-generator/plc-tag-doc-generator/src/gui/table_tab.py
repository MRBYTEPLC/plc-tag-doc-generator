"""
table_tab.py
--------------
Generic Treeview-based tab used to display tags and routines in a
sortable, filterable table.
"""

import tkinter as tk
from tkinter import ttk


class TableTab(ttk.Frame):
    def __init__(self, parent, columns, headers, widths):
        super().__init__(parent, padding=10)
        self.columns = columns

        filter_row = ttk.Frame(self)
        filter_row.pack(fill="x", pady=(0, 8))
        ttk.Label(filter_row, text="Filter:").pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *_: self._apply_filter())
        entry = ttk.Entry(filter_row, textvariable=self.filter_var, width=40)
        entry.pack(side="left", padx=(6, 0))

        self.count_lbl = ttk.Label(filter_row, text="")
        self.count_lbl.pack(side="right")

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=headers[col],
                               command=lambda c=col: self._sort_by(c, False))
            self.tree.column(col, width=widths.get(col, 120), anchor="w")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._all_rows = []

    def load_rows(self, rows):
        """rows: list of tuples matching self.columns order."""
        self._all_rows = rows
        self._render(rows)

    def _render(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.count_lbl.config(text=f"{len(rows)} row(s)")

    def _apply_filter(self):
        query = self.filter_var.get().lower().strip()
        if not query:
            self._render(self._all_rows)
            return
        filtered = [
            row for row in self._all_rows
            if any(query in str(cell).lower() for cell in row)
        ]
        self._render(filtered)

    def _sort_by(self, col, reverse):
        idx = self.columns.index(col)
        try:
            self._all_rows.sort(key=lambda r: str(r[idx]).lower(), reverse=reverse)
        except Exception:
            pass
        self._apply_filter()
        self.tree.heading(col, command=lambda: self._sort_by(col, not reverse))
