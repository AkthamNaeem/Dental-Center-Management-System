from tkinter import ttk
from .base import BaseTab
from .style import STYLE

class RecordsTab(BaseTab):
    def _create_widgets(self):
        header = ttk.Label(self, text="السجلات الطبية", style="Header.TLabel")
        header.pack(pady=(STYLE["pad_section"], STYLE["pad_y"]))

        columns = ("id", "patient", "treatment", "date")
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", height=STYLE["table_height"], selectmode="browse"
        )
        for col, text in zip(columns, ("#", "المريض", "المعالجة", "التاريخ")):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=STYLE["table_column_width"].get(col, STYLE["table_column_width"]["default"]))

        self.tree.pack(fill="both", expand=True, padx=STYLE["pad_x"])

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=STYLE["pad_y"])

        ttk.Button
