from tkinter import ttk
from .base import BaseTab
from .style import STYLE

class PatientsTab(BaseTab):
    def _create_widgets(self):
        header = ttk.Label(self, text="إدارة المرضى", style="Header.TLabel")
        header.pack(pady=(STYLE["pad_section"], STYLE["pad_y"]))

        columns = ("id", "name", "dob", "phone")
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", height=STYLE["table_height"], selectmode="browse"
        )
        for col, text in zip(columns, ("#", "الاسم", "تاريخ الميلاد", "الهاتف")):
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor="center", width=STYLE["table_column_width"].get(col, STYLE["table_column_width"]["default"]))

        self.tree.pack(fill="both", expand=True, padx=STYLE["pad_x"])

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=STYLE["pad_y"])

        ttk.Button(btn_frame, text="إضافة مريض", command=self.add_patient).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="تعديل", command=self.edit_patient).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="حذف", command=self.delete_patient).pack(side="left", padx=5)

    def add_patient(self):
        self.flash("ميزة إضافة مريض قيد التطوير ✨")
    def edit_patient(self):
        self.flash("ميزة التعديل قيد التطوير", kind="warning")
    def delete_patient(self):
        self.flash("ميزة الحذف قيد التطوير", kind="warning")
