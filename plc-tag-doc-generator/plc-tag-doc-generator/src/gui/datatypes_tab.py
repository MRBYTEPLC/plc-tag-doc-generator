"""
datatypes_tab.py
------------------
Displays user-defined data types (UDTs) as an expandable tree: each
DataType is a top-level node, its Members are child rows.
"""

from tkinter import ttk


class DataTypesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self._build()

    def _build(self):
        self.count_lbl = ttk.Label(self, text="")
        self.count_lbl.pack(anchor="w", pady=(0, 8))

        columns = ("data_type", "access", "description")
        self.tree = ttk.Treeview(self, columns=columns, show="tree headings")
        self.tree.heading("#0", text="Name")
        self.tree.heading("data_type", text="Data Type")
        self.tree.heading("access", text="External Access")
        self.tree.heading("description", text="Description")
        self.tree.column("#0", width=220, anchor="w")
        self.tree.column("data_type", width=140, anchor="w")
        self.tree.column("access", width=120, anchor="w")
        self.tree.column("description", width=400, anchor="w")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

    def load_data_types(self, data_types):
        self.tree.delete(*self.tree.get_children())
        for dt in data_types:
            parent_id = self.tree.insert(
                "", "end", text=dt["name"], open=False,
                values=("(User-Defined Type)", "", dt["description"])
            )
            for member in dt["members"]:
                self.tree.insert(
                    parent_id, "end", text=member["name"],
                    values=(member["data_type"], member["external_access"], member["description"])
                )
        self.count_lbl.config(text=f"{len(data_types)} data type(s)")
