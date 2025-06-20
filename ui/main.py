import tkinter as tk
from tkinter import ttk
from models import Doctor, Patient, Record
from .header import Header
from .doctor_view import DoctorView
from .doctor_detail_view import DoctorDetailView
from .patient_view import PatientView
from .patient_detail_view import PatientDetailView
from .record_view import RecordView
from .record_detail_view import RecordDetailView

class DentalCenterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dental Center Management System")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("Header.TFrame", background="#4a6fa5")
        self.style.configure("Header.TLabel", background="#4a6fa5", foreground="white", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", font=("Arial", 10))
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.map("Treeview", background=[("selected", "#347083")])

        # Create header
        self.header = Header(self, self.on_search_select)
        self.header.pack(fill=tk.X, padx=10, pady=5)

        # Create main content area
        self.main_content = ttk.Frame(self)
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Navigation buttons
        self.nav_frame = ttk.Frame(self.main_content)
        self.nav_frame.pack(fill=tk.X, pady=5)

        self.doctors_btn = ttk.Button(self.nav_frame, text="Doctors", command=self.show_doctors)
        self.doctors_btn.pack(side=tk.LEFT, padx=5)

        self.patients_btn = ttk.Button(self.nav_frame, text="Patients", command=self.show_patients)
        self.patients_btn.pack(side=tk.LEFT, padx=5)

        self.records_btn = ttk.Button(self.nav_frame, text="Records", command=self.show_records)
        self.records_btn.pack(side=tk.LEFT, padx=5)

        # Current view
        self.current_view = None

        # Show doctors by default
        self.show_doctors()

    def show_doctors(self):
        self.clear_main_content()
        self.current_view = DoctorView(self.main_content, self.show_doctor_detail)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_patients(self):
        self.clear_main_content()
        self.current_view = PatientView(self.main_content, self.show_patient_detail)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_records(self):
        self.clear_main_content()
        self.current_view = RecordView(self.main_content, self.show_record_detail)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_doctor_detail(self, doctor_id):
        self.clear_main_content()
        self.current_view = DoctorDetailView(self.main_content, doctor_id, self.show_doctors)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_patient_detail(self, patient_id):
        self.clear_main_content()
        self.current_view = PatientDetailView(self.main_content, patient_id, self.show_patients)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def show_record_detail(self, record_id):
        self.clear_main_content()
        self.current_view = RecordDetailView(self.main_content, record_id, self.show_records)
        self.current_view.pack(fill=tk.BOTH, expand=True)

    def clear_main_content(self):
        if self.current_view:
            self.current_view.destroy()

    def on_search_select(self, item_type, item_id):
        if item_type == "doctor":
            self.show_doctor_detail(item_id)
        elif item_type == "patient":
            self.show_patient_detail(item_id)
        elif item_type == "record":
            self.show_record_detail(item_id)

def run():
    app = DentalCenterApp()
    app.mainloop()

if __name__ == "__main__":
    run()
