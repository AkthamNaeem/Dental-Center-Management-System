import tkinter as tk
from tkinter import ttk
from datetime import datetime
from models import Record, Treatment, Payment
from .dialogs import TreatmentFormDialog, PaymentFormDialog
from utils.pdf_exporter import export_record_to_pdf

class RecordDetailView(ttk.Frame):
    def __init__(self, parent, record_id, on_back):
        super().__init__(parent)
        self.record_id = record_id
        self.on_back = on_back

        self.create_widgets()
        self.load_record()
        self.load_treatments()
        self.load_payments()

    def create_widgets(self):
        # Header with back button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=5)

        back_btn = ttk.Button(header_frame, text="← Back", command=self.on_back)
        back_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(header_frame, text="Export to PDF", command=self.export_to_pdf)
        export_btn.pack(side=tk.RIGHT, padx=5)

        delete_btn = ttk.Button(header_frame, text="Delete", command=self.delete_record)
        delete_btn.pack(side=tk.RIGHT, padx=5)

        # Record info
        self.info_frame = ttk.LabelFrame(self, text="Record Information")
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Financial summary frame
        finance_frame = ttk.LabelFrame(self, text="Financial Summary")
        finance_frame.pack(fill=tk.X, padx=10, pady=5)

        # Total treatments label
        self.total_treatments_label = ttk.Label(finance_frame, text="Total Treatments: $0.00")
        self.total_treatments_label.pack(anchor=tk.W)

        # Total payments label
        self.total_payments_label = ttk.Label(finance_frame, text="Total Payments: $0.00")
        self.total_payments_label.pack(anchor=tk.W)

        # Balance label
        self.balance_label = ttk.Label(finance_frame, text="Balance: $0.00", font=("Arial", 10, "bold"))
        self.balance_label.pack(anchor=tk.W)

        # Treatments section
        treatments_frame = ttk.LabelFrame(self, text="Treatments")
        treatments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treatments toolbar
        treatments_toolbar = ttk.Frame(treatments_frame)
        treatments_toolbar.pack(fill=tk.X)

        add_treatment_btn = ttk.Button(treatments_toolbar, text="Add Treatment", command=self.add_treatment)
        add_treatment_btn.pack(side=tk.LEFT, padx=5)

        # Treatments table
        self.treatments_tree = ttk.Treeview(
            treatments_frame,
            columns=("id", "name", "cost", "date", "notes"),
            show="headings"
        )
        self.treatments_tree.heading("id", text="ID")
        self.treatments_tree.heading("name", text="Treatment Name")
        self.treatments_tree.heading("cost", text="Cost")
        self.treatments_tree.heading("date", text="Date")
        self.treatments_tree.heading("notes", text="Notes")

        self.treatments_tree.column("id", width=50, anchor=tk.CENTER)
        self.treatments_tree.column("name", width=200)
        self.treatments_tree.column("cost", width=80, anchor=tk.CENTER)
        self.treatments_tree.column("date", width=100, anchor=tk.CENTER)
        self.treatments_tree.column("notes", width=250)

        treatments_scrollbar = ttk.Scrollbar(treatments_frame, orient=tk.VERTICAL, command=self.treatments_tree.yview)
        self.treatments_tree.configure(yscrollcommand=treatments_scrollbar.set)

        self.treatments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        treatments_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Payments section
        payments_frame = ttk.LabelFrame(self, text="Payments")
        payments_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Payments toolbar
        payments_toolbar = ttk.Frame(payments_frame)
        payments_toolbar.pack(fill=tk.X)

        add_payment_btn = ttk.Button(payments_toolbar, text="Add Payment", command=self.add_payment)
        add_payment_btn.pack(side=tk.LEFT, padx=5)

        # Payments table
        self.payments_tree = ttk.Treeview(
            payments_frame,
            columns=("id", "amount", "method", "date", "notes"),
            show="headings"
        )
        self.payments_tree.heading("id", text="ID")
        self.payments_tree.heading("amount", text="Amount")
        self.payments_tree.heading("method", text="Method")
        self.payments_tree.heading("date", text="Date")
        self.payments_tree.heading("notes", text="Notes")

        self.payments_tree.column("id", width=50, anchor=tk.CENTER)
        self.payments_tree.column("amount", width=80, anchor=tk.CENTER)
        self.payments_tree.column("method", width=80, anchor=tk.CENTER)
        self.payments_tree.column("date", width=100, anchor=tk.CENTER)
        self.payments_tree.column("notes", width=250)

        payments_scrollbar = ttk.Scrollbar(payments_frame, orient=tk.VERTICAL, command=self.payments_tree.yview)
        self.payments_tree.configure(yscrollcommand=payments_scrollbar.set)

        self.payments_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        payments_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Balance label
        # self.balance_label = ttk.Label(self, text="Balance: $0.00", font=("Arial", 12, "bold"))
        # self.balance_label.pack(pady=10)

    def load_record(self):
        record = Record.get_by_id(self.record_id)
        if not record:
            self.on_back()
            return

        # Clear previous info
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Add record info
        info_labels = [
            ("Doctor:", f"{record.doctor.name} ({record.doctor.specialty or 'No specialty'})"),
            ("Patient:", record.patient.name),
            ("Created At:", record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else "N/A")
        ]

        for i, (label, value) in enumerate(info_labels):
            ttk.Label(self.info_frame, text=label, font=("Arial", 10, "bold")).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Label(self.info_frame, text=value).grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)

    def load_treatments(self):
        for item in self.treatments_tree.get_children():
            self.treatments_tree.delete(item)

        record = Record.get_by_id(self.record_id)
        if not record:
            return

        treatments = record.get_treatments()
        for treatment in treatments:
            # Ensure treatment_date is properly handled
            if isinstance(treatment.treatment_date, str):
                try:
                    treatment_date = datetime.strptime(treatment.treatment_date, "%Y-%m-%d %H:%M:%S")
                except (ValueError, TypeError):
                    treatment_date = None
            else:
                treatment_date = treatment.treatment_date

            self.treatments_tree.insert("", tk.END, values=(
                treatment.id,
                treatment.treatment_name,
                f"${treatment.cost:.2f}",
                treatment_date.strftime("%Y-%m-%d") if treatment_date else "",
                treatment.notes or ""
            ))

        self.update_balance()
        self.update_financial_summary()

    def load_payments(self):
        for item in self.payments_tree.get_children():
            self.payments_tree.delete(item)

        record = Record.get_by_id(self.record_id)
        if not record:
            return

        payments = record.get_payments()
        for payment in payments:
            self.payments_tree.insert("", tk.END, values=(
                payment.id,
                f"${payment.amount:.2f}",
                payment.payment_method,
                payment.payment_date.strftime("%Y-%m-%d") if payment.payment_date else "",
                payment.notes or ""
            ))

        self.update_balance()
        self.update_financial_summary()

    def update_balance(self):
        record = Record.get_by_id(self.record_id)
        if not record:
            return

        # balance = record.get_balance()
        # print(f"update balance: ${balance:.2f}")
        # if balance > 0:
        #     self.balance_label.config(text=f"Balance Due: ${balance:.2f}", foreground="red")
        # elif balance < 0:
        #     self.balance_label.config(text=f"Credit: ${-balance:.2f}", foreground="green")
        # else:
        #     self.balance_label.config(text="Balance: $0.00", foreground="black")

    def add_treatment(self):
        def on_success():
            self.load_treatments()

        dialog = TreatmentFormDialog(self, self.record_id, on_success)
        dialog.show()

    def add_payment(self):
        def on_success():
            self.load_payments()

        dialog = PaymentFormDialog(self, self.record_id, on_success)
        dialog.show()

    def export_to_pdf(self):
        record = Record.get_by_id(self.record_id)
        if record:
            try:
                from utils.pdf_exporter import export_record_to_pdf
                filename = export_record_to_pdf(record)
                tk.messagebox.showinfo("Success", f"Record exported to {filename}")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")

    def delete_record(self):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to delete this record and all its treatments and payments?"):
            try:
                if Record.delete(self.record_id):
                    self.on_back()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Could not delete record: {e}")

    def update_financial_summary(self):
        record = Record.get_by_id(self.record_id)
        if not record:
            return

        # Force fresh calculations
        treatments = record.get_treatments()
        payments = record.get_payments()

        total_treatments = sum(t.cost for t in treatments)
        total_payments = sum(p.amount for p in payments)
        balance = total_treatments - total_payments


        # Update UI
        self.total_treatments_label.config(text=f"Total Treatments: ${total_treatments:.2f}")
        self.total_payments_label.config(text=f"Total Payments: ${total_payments:.2f}")
        self.balance_label.config(text=f"Balance: ${balance:.2f}")

        # Color coding
        if balance > 0:
            self.balance_label.config(foreground="red")
        elif balance < 0:
            self.balance_label.config(foreground="green")
        else:
            self.balance_label.config(foreground="black")

        print(f"UI Updated - Treatments: ${total_treatments:.2f}, Payments: ${total_payments:.2f}, Balance: ${balance:.2f}")  # Debug
