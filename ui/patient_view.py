import tkinter as tk
from tkinter import ttk
from models import Patient
from .dialogs import PatientFormDialog

class PatientView(ttk.Frame):
    def __init__(self, parent, on_patient_select):
        super().__init__(parent)
        self.on_patient_select = on_patient_select

        self.create_widgets()
        self.load_patients()

    def create_widgets(self):
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=5)

        add_btn = ttk.Button(toolbar, text="Add Patient", command=self.add_patient)
        add_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(toolbar, text="Refresh", command=self.load_patients)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Patients table
        self.tree = ttk.Treeview(self, columns=("id", "name", "phone", "gender", "birth_date"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("birth_date", text="Birth Date")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=200)
        self.tree.column("phone", width=120)
        self.tree.column("gender", width=80, anchor=tk.CENTER)
        self.tree.column("birth_date", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.on_double_click)

    def load_patients(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        patients = Patient.get_all()
        for pat in patients:
            self.tree.insert("", tk.END, values=(
                pat.id, pat.name, pat.phone or "", pat.gender or "",
                pat.birth_date.strftime("%Y-%m-%d") if pat.birth_date else ""
            ))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        patient_id = self.tree.item(item, "values")[0]
        self.on_patient_select(patient_id)

    def add_patient(self):
        def on_success():
            self.load_patients()

        dialog = PatientFormDialog(self, on_success)
        dialog.show()
