import tkinter as tk
from tkinter import ttk
from models import Doctor, Patient, Record


class Header(ttk.Frame):
    def __init__(self, parent, on_select_callback):
        super().__init__(parent)
        self.on_select_callback = on_select_callback
        self.search_results_shown = False
        self._search_results_data = []

        # Search frame
        self.search_frame = ttk.Frame(self)
        self.search_frame.pack(side=tk.RIGHT, padx=10, pady=5)

        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.search_frame,
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", self.on_search_change)

        # Search results dropdown
        self.search_results = tk.Listbox(
            self,
            bg="white",
            bd=1,
            relief=tk.SOLID,
            highlightthickness=0,
            selectbackground="#347083",
            selectforeground="white",
            font=("Arial", 10),
            activestyle='none'
        )
        self.search_results.bind("<<ListboxSelect>>", self.on_search_select)

    def on_search_change(self, event):
        search_term = self.search_var.get().strip()
        if not search_term:
            self.hide_search_results()
            return

        results = self.perform_search(search_term)
        self.update_search_results(results)

    def perform_search(self, search_term):
        results = []

        # Search doctors
        doctors = Doctor.search(search_term)
        results.extend(("doctor", doc.id, f"[Doctor] {doc.name}") for doc in doctors)

        # Search patients
        patients = Patient.search(search_term)
        results.extend(("patient", pat.id, f"[Patient] {pat.name}") for pat in patients)

        # Search records by doctor
        for doc in doctors:
            for rec in Record.get_by_doctor(doc.id):
                results.append(("record", rec.id, f"[Record] {rec.doctor_name} - {rec.patient_name}"))

        # Search records by patient
        for pat in patients:
            for rec in Record.get_by_patient(pat.id):
                results.append(("record", rec.id, f"[Record] {rec.doctor_name} - {rec.patient_name}"))

        return results

    def update_search_results(self, results):
        self.search_results.delete(0, tk.END)
        self._search_results_data = results

        if not results:
            self.hide_search_results()
            return

        for i, item in enumerate(results[:10]):
            self.search_results.insert(tk.END, item[2])
            color = 'blue' if item[0] == 'doctor' else 'green' if item[0] == 'patient' else 'black'
            bg_color = 'white' if i % 2 == 0 else '#f5f5f5'
            self.search_results.itemconfig(tk.END, {
                'fg': color,
                'bg': bg_color
            })

        if results:
            self.show_search_results()

    def show_search_results(self):
        if not self.search_results_shown and self.search_results.size() > 0:
            # Calculate position relative to search entry
            x = self.search_entry.winfo_x()
            y = self.search_entry.winfo_y() + self.search_entry.winfo_height()
            width = self.search_entry.winfo_width()
            height = min(10, self.search_results.size()) * 20 + 4

            # Position dropdown
            self.search_results.place(
                x=x,
                y=y,
                width=width,
                height=height
            )
            self.search_results.lift()
            self.search_results_shown = True

    def hide_search_results(self):
        if self.search_results_shown:
            self.search_results.place_forget()
            self.search_results_shown = False

    def on_search_select(self, event):
        if not self.search_results.curselection():
            return

        index = self.search_results.curselection()[0]
        if 0 <= index < len(self._search_results_data):
            item_type, item_id, _ = self._search_results_data[index]
            self.on_select_callback(item_type, item_id)
            self.hide_search_results()
            self.search_var.set("")
