import tkinter as tk
from tkinter import ttk
from models import Doctor, Record
from .dialogs import DoctorFormDialog

class DoctorDetailView(ttk.Frame):
    def __init__(self, parent, doctor_id, on_back):
        super().__init__(parent)
        self.doctor_id = doctor_id
        self.on_back = on_back

        self.create_widgets()
        self.load_doctor()
        self.load_records()

    def create_widgets(self):
        # Header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=5)

        back_btn = ttk.Button(header_frame, text="← Back", command=self.on_back)
        back_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ttk.Button(header_frame, text="Edit", command=self.edit_doctor)
        edit_btn.pack(side=tk.RIGHT, padx=5)

        delete_btn = ttk.Button(header_frame, text="Delete", command=self.delete_doctor)
        delete_btn.pack(side=tk.RIGHT, padx=5)

        # Doctor info
        self.info_frame = ttk.LabelFrame(self, text="Doctor Information")
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Records section
        records_frame = ttk.LabelFrame(self, text="Patient Records")
        records_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Records table
        self.tree = ttk.Treeview(records_frame, columns=("id", "patient", "created"), show="headings")
        self.tree.heading("id", text="Record ID")
        self.tree.heading("patient", text="Patient")
        self.tree.heading("created", text="Created At")

        self.tree.column("id", width=80, anchor=tk.CENTER)
        self.tree.column("patient", width=250)
        self.tree.column("created", width=150, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(records_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.on_record_select)

    def load_doctor(self):
        doctor = Doctor.get_by_id(self.doctor_id)
        if not doctor:
            self.on_back()
            return

        # Clear previous info
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Add doctor info
        info_labels = [
            ("Name:", doctor.name),
            ("Specialty:", doctor.specialty or "N/A"),
            ("Phone:", doctor.phone or "N/A"),
            ("Email:", doctor.email or "N/A"),
            ("Created At:", doctor.created_at.strftime("%Y-%m-%d %H:%M") if doctor.created_at else "N/A")
        ]

        for i, (label, value) in enumerate(info_labels):
            ttk.Label(self.info_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Label(self.info_frame, text=value).grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        records = Record.get_by_doctor(self.doctor_id)
        for rec in records:
            self.tree.insert("", tk.END, values=(
                rec.id, rec.patient_name,
                rec.created_at.strftime("%Y-%m-%d %H:%M") if rec.created_at else ""
            ))

    def on_record_select(self, event):
        item = self.tree.selection()[0]
        record_id = self.tree.item(item, "values")[0]
        self.master.master.show_record_detail(record_id)

    def edit_doctor(self):
        doctor = Doctor.get_by_id(self.doctor_id)
        if not doctor:
            return

        def on_success():
            self.load_doctor()

        dialog = DoctorFormDialog(self, on_success)

        # Pre-fill the form
        dialog.name_entry.insert(0, doctor.name)
        if doctor.specialty:
            dialog.specialty_entry.insert(0, doctor.specialty)
        if doctor.phone:
            dialog.phone_entry.insert(0, doctor.phone)
        if doctor.email:
            dialog.email_entry.insert(0, doctor.email)

        dialog.show()

    def delete_doctor(self):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to delete this doctor?"):
            try:
                if Doctor.delete(self.doctor_id):
                    self.on_back()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not delete doctor: {e}")
