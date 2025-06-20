import tkinter as tk
from tkinter import ttk
from models import Doctor
from .dialogs import DoctorFormDialog

class DoctorView(ttk.Frame):
    def __init__(self, parent, on_doctor_select):
        super().__init__(parent)
        self.on_doctor_select = on_doctor_select

        self.create_widgets()
        self.load_doctors()

    def create_widgets(self):
        # Toolbar
        toolbar = ttk.Frame(self)
        toolbar.pack(fill=tk.X, pady=5)

        add_btn = ttk.Button(toolbar, text="Add Doctor", command=self.add_doctor)
        add_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(toolbar, text="Refresh", command=self.load_doctors)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Doctors table
        self.tree = ttk.Treeview(self, columns=("id", "name", "specialty", "phone", "email"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("specialty", text="Specialty")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("email", text="Email")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("name", width=200)
        self.tree.column("specialty", width=150)
        self.tree.column("phone", width=120)
        self.tree.column("email", width=200)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.on_double_click)

    def load_doctors(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        doctors = Doctor.get_all()
        for doc in doctors:
            self.tree.insert("", tk.END, values=(
                doc.id, doc.name, doc.specialty or "", doc.phone or "", doc.email or ""
            ))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        doctor_id = self.tree.item(item, "values")[0]
        self.on_doctor_select(doctor_id)

    def add_doctor(self):
        def on_success():
            self.load_doctors()

        dialog = DoctorFormDialog(self, on_success)
        dialog.show()
