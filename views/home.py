import tkinter as tk
from tkinter import ttk
from .base import BaseTab
from .style import STYLE

class HomeTab(BaseTab):
    """صفحة البحث العامة مع فلترة حسب النموذج."""

    def _create_widgets(self):
        # إطار البحث
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=STYLE["pad_x"], pady=(STYLE["pad_section"], STYLE["pad_y"]))

        ttk.Label(search_frame, text="بحث:").pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=STYLE["entry_width"])
        search_entry.pack(side="left", padx=(5, 15))
        search_entry.bind("<KeyRelease>", self.on_search)
        search_entry.bind("<Return>", self.on_search)

        ttk.Label(search_frame, text="النطاق:").pack(side="left")
        self.filter_var = tk.StringVar(value="الكل")
        filter_combo = ttk.Combobox(
            search_frame,
            textvariable=self.filter_var,
            state="readonly",
            width=STYLE["combo_width"],
            values=("الكل", "الأطباء", "المرضى", "السجلات"),
        )
        filter_combo.pack(side="left")
        filter_combo.bind("<<ComboboxSelected>>", self.on_search)

        # جدول النتائج
        columns = ("model", "primary", "secondary")
        self.results = ttk.Treeview(self, columns=columns, show="headings", height=STYLE["table_height"])
        for col, text in zip(columns, ("النموذج", "القيمة", "وصف إضافي")):
            width = STYLE["table_column_width"].get(col, STYLE["table_column_width"]["default"])
            self.results.heading(col, text=text)
            self.results.column(col, anchor="center", width=width)

        self.results.pack(fill="both", expand=True, padx=STYLE["pad_x"], pady=STYLE["pad_y"])

    # ——— بحث مزيّف إلى حين ربط الخدمات ———
    def on_search(self, event=None):
        query = self.search_var.get().strip()
        model_filter = self.filter_var.get()
        self.results.delete(*self.results.get_children())
        if not query:
            return
        for row in self._dummy_search(query, model_filter):
            self.results.insert("", "end", values=row)

    def _dummy_search(self, query: str, model_filter: str):
        sample = [
            ("الأطباء", "د. أحمد", "اختصاص: حشوات"),
            ("المرضى", "محمد علي", "مواليد 1985‑03‑12"),
            ("السجلات", "خلع ضرس", "بتاريخ 2025‑05‑12"),
            ("الأطباء", "د. خالد", "اختصاص: تقويم"),
            ("المرضى", "سمر حسن", "مواليد 1990‑08‑02"),
        ]
        if model_filter != "الكل":
            sample = [r for r in sample if r[0] == model_filter]
        return [r for r in sample if query.lower() in r[1].lower()]
