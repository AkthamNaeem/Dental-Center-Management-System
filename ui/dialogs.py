import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models import Doctor, Patient, Record, Treatment, Payment

class DoctorFormDialog:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Doctor")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        self.create_form()

    def create_form(self):
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Specialty
        ttk.Label(form_frame, text="Specialty:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.specialty_entry = ttk.Entry(form_frame, width=30)
        self.specialty_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Email
        ttk.Label(form_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_doctor)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def save_doctor(self):
        name = self.name_entry.get().strip()
        specialty = self.specialty_entry.get().strip() or None
        phone = self.phone_entry.get().strip() or None
        email = self.email_entry.get().strip() or None

        if not name:
            messagebox.showerror("Error", "Name is required")
            return

        try:
            Doctor.create(name, specialty, phone, email)
            self.on_success()
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

class PatientFormDialog:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Patient")
        self.dialog.geometry("400x400")
        self.dialog.resizable(False, False)

        self.create_form()

    def create_form(self):
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Name
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Phone
        ttk.Label(form_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Gender
        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.gender_var = tk.StringVar()
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=2, column=1, sticky=tk.W)

        ttk.Radiobutton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side=tk.LEFT)
        ttk.Radiobutton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(side=tk.LEFT)

        # Birth Date
        ttk.Label(form_frame, text="Birth Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.birth_date_entry = ttk.Entry(form_frame, width=30)
        self.birth_date_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Address
        ttk.Label(form_frame, text="Address:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.address_entry = ttk.Entry(form_frame, width=30)
        self.address_entry.grid(row=4, column=1, sticky=tk.W, pady=5)

        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Text(form_frame, width=30, height=4)
        self.notes_entry.grid(row=5, column=1, sticky=tk.W, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_patient)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def save_patient(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        gender = self.gender_var.get() or None
        birth_date = self.birth_date_entry.get().strip() or None
        address = self.address_entry.get().strip() or None
        notes = self.notes_entry.get("1.0", tk.END).strip() or None

        if not name:
            messagebox.showerror("Error", "Name is required")
            return
        if not phone:
            messagebox.showerror("Error", "Phone is required")
            return

        try:
            Patient.create(name, phone, gender, birth_date, address, notes)
            self.on_success()
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

class RecordFormDialog:
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Record")
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)

        self.create_form()

    def create_form(self):
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Doctor
        ttk.Label(form_frame, text="Doctor:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.doctor_var = tk.StringVar()
        self.doctor_combo = ttk.Combobox(form_frame, textvariable=self.doctor_var, state="readonly")
        self.doctor_combo.grid(row=0, column=1, sticky=tk.W, pady=5)

        doctors = Doctor.get_all()
        self.doctor_combo["values"] = [f"{doc.id}: {doc.name}" for doc in doctors]
        if doctors:
            self.doctor_combo.current(0)

        # Patient
        ttk.Label(form_frame, text="Patient:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(form_frame, textvariable=self.patient_var, state="readonly")
        self.patient_combo.grid(row=1, column=1, sticky=tk.W, pady=5)

        patients = Patient.get_all()
        self.patient_combo["values"] = [f"{pat.id}: {pat.name}" for pat in patients]
        if patients:
            self.patient_combo.current(0)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_record)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def save_record(self):
        doctor_str = self.doctor_var.get()
        patient_str = self.patient_var.get()

        if not doctor_str or not patient_str:
            messagebox.showerror("Error", "Both doctor and patient are required")
            return

        try:
            doctor_id = int(doctor_str.split(":")[0].strip())
            patient_id = int(patient_str.split(":")[0].strip())

            Record.create(doctor_id, patient_id)
            self.on_success()
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

class TreatmentFormDialog:
    def __init__(self, parent, record_id, on_success):
        self.parent = parent
        self.record_id = record_id
        self.on_success = on_success
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Treatment")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        self.create_form()

    def create_form(self):
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Treatment Name
        ttk.Label(form_frame, text="Treatment Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Cost
        ttk.Label(form_frame, text="Cost:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cost_entry = ttk.Entry(form_frame, width=30)
        self.cost_entry.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Treatment Date
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=30)
        self.date_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Text(form_frame, width=30, height=4)
        self.notes_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_treatment)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def save_treatment(self):
        name = self.name_entry.get().strip()
        cost_str = self.cost_entry.get().strip()
        date_str = self.date_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip() or None

        if not name:
            messagebox.showerror("Error", "Treatment name is required")
            return
        if not cost_str:
            messagebox.showerror("Error", "Cost is required")
            return

        try:
            cost = float(cost_str)
            if cost <= 0:
                raise ValueError("Cost must be positive")

            treatment_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else None

            Treatment.create(self.record_id, name, cost, treatment_date, notes)
            self.on_success()
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

class PaymentFormDialog:
    def __init__(self, parent, record_id, on_success):
        self.parent = parent
        self.record_id = record_id
        self.on_success = on_success
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Payment")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        self.create_form()

    def create_form(self):
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Amount
        ttk.Label(form_frame, text="Amount:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.amount_entry = ttk.Entry(form_frame, width=30)
        self.amount_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Payment Method
        ttk.Label(form_frame, text="Payment Method:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.method_var = tk.StringVar(value="Cash")
        method_frame = ttk.Frame(form_frame)
        method_frame.grid(row=1, column=1, sticky=tk.W)

        ttk.Radiobutton(method_frame, text="Cash", variable=self.method_var, value="Cash").pack(side=tk.LEFT)
        ttk.Radiobutton(method_frame, text="Card", variable=self.method_var, value="Card").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(method_frame, text="Other", variable=self.method_var, value="Other").pack(side=tk.LEFT)

        # Payment Date
        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(form_frame, width=30)
        self.date_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Text(form_frame, width=30, height=4)
        self.notes_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        save_btn = ttk.Button(button_frame, text="Save", command=self.save_payment)
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def save_payment(self):
        amount_str = self.amount_entry.get().strip()
        method = self.method_var.get()
        date_str = self.date_entry.get().strip()
        notes = self.notes_entry.get("1.0", tk.END).strip() or None

        if not amount_str:
            messagebox.showerror("Error", "Amount is required")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Amount must be positive")

            payment_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else None

            Payment.create(self.record_id, amount, method, payment_date, notes)
            self.on_success()
            self.dialog.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)
