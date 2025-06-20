import tkinter as tk
from tkinter import ttk
from models import Patient, Record
from .dialogs import PatientFormDialog

class PatientDetailView(ttk.Frame):
    def __init__(self, parent, patient_id, on_back):
        super().__init__(parent)
        self.patient_id = patient_id
        self.on_back = on_back

        self.create_widgets()
        self.load_patient()
        self.load_records()

    def create_widgets(self):
        # Header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=5)

        back_btn = ttk.Button(header_frame, text="← Back", command=self.on_back)
        back_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ttk.Button(header_frame, text="Edit", command=self.edit_patient)
        edit_btn.pack(side=tk.RIGHT, padx=5)

        delete_btn = ttk.Button(header_frame, text="Delete", command=self.delete_patient)
        delete_btn.pack(side=tk.RIGHT, padx=5)

        # Patient info
        self.info_frame = ttk.LabelFrame(self, text="Patient Information")
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Records section
        records_frame = ttk.LabelFrame(self, text="Doctor Records")
        records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Records table
        self.tree = ttk.Treeview(records_frame, columns=("id", "doctor", "created"), show="headings")
        self.tree.heading("id", text="Record ID")
        self.tree.heading("doctor", text="Doctor")
        self.tree.heading("created", text="Created At")

        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("doctor", width=250)
        self.tree.column("created", width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.on_record_select)

    def load_patient(self):
        patient = Patient.get_by_id(self.patient_id)
        if not patient:
            self.on_back()
            return

        # Clear previous info
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Add patient info
        info_labels = [
            ("Name:", patient.name),
            ("Phone:", patient.phone or "N/A"),
            ("Gender:", patient.gender or "N/A"),
            ("Birth Date:", patient.birth_date.strftime("%Y-%m-%d") if patient.birth_date else "N/A"),
            ("Address:", patient.address or "N/A"),
            ("Notes:", patient.notes or "N/A"),
            ("Created At:", patient.created_at.strftime("%Y-%m-%d %H:%M") if patient.created_at else "N/A")
        ]

        for i, (label, value) in enumerate(info_labels):
            ttk.Label(self.info_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Label(self.info_frame, text=value).grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = Record.get_by_patient(self.patient_id)
        for rec in records:
            self.tree.insert("", tk.END, values=(
                rec.id, rec.doctor_name,
                rec.created_at.strftime("%Y-%m-%d %H:%M") if rec.created_at else ""
            ))

    def on_record_select(self, event):
        item = self.tree.selection()[0]
        record_id = self.tree.item(item, "values")[0]
        self.master.master.show_record_detail(record_id)

    def edit_patient(self):
        patient = Patient.get_by_id(self.patient_id)
        if not patient:
            return

        def on_success():
            self.load_patient()

        dialog = PatientFormDialog(self, on_success)

        # Pre-fill the form
        dialog.name_entry.insert(0, patient.name)
        dialog.phone_entry.insert(0, patient.phone)
        if patient.gender:
            dialog.gender_var.set(patient.gender)
        if patient.birth_date:
            dialog.birth_date_entry.insert(0, patient.birth_date.strftime("%Y-%m-%d"))
        if patient.address:
            dialog.address_entry.insert(0, patient.address)
        if patient.notes:
            dialog.notes_entry.insert("1.0", patient.notes)

        dialog.show()

    def delete_patient(self):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to delete this patient?"):
            try:
                if Patient.delete(self.patient_id):
                    self.on_back()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not delete patient: {e}")
