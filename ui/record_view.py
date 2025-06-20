import tkinter as tk
from tkinter import ttk
from models import Record
from .dialogs import RecordFormDialog

class RecordView(ttk.Frame):
    def __init__(self, parent, on_record_select):
        super().__init__(parent)
        self.on_record_select = on_record_select

        self.create_widgets()
        self.load_records()

    def create_widgets(self):
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=5)

        add_btn = ttk.Button(toolbar, text="Add Record", command=self.add_record)
        add_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(toolbar, text="Refresh", command=self.load_records)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Records table
        self.tree = ttk.Treeview(self, columns=("id", "doctor", "patient", "created", "total"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("doctor", text="Doctor")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("created", text="Created At")
        self.tree.heading("total", text="Total Amount")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("doctor", width=200)
        self.tree.column("patient", width=200)
        self.tree.column("created", width=150, anchor=tk.CENTER)
        self.tree.column("total", width=100, anchor=tk.E)  # Right-aligned for amounts

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.on_double_click)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = Record.get_all()
        for rec in records:
            self.tree.insert("", tk.END, values=(
                rec.id,
                rec.doctor_name,
                rec.patient_name,
                rec.created_at.strftime("%Y-%m-%d %H:%M") if rec.created_at else "",
                f"${rec.total_amount:.2f}"  # Format as currency
            ))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        record_id = self.tree.item(item, "values")[0]
        self.on_record_select(record_id)

    def add_record(self):
        def on_success():
            self.load_records()

        dialog = RecordFormDialog(self, on_success)
        dialog.show()

