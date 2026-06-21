import tkinter as tk
from tkinter import ttk, messagebox


class AddInsuranceDialog(tk.Toplevel):
    def __init__(self, parent, fleet_manager, callback):
        super().__init__(parent)
        self.title("Add Insurance Record")
        self.geometry("450x350")
        self.fleet_manager = fleet_manager
        self.callback = callback
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Car ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.car_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.car_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Provider:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.provider_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.provider_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Policy Number:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.policy_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.policy_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Coverage Type:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.coverage_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.coverage_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.start_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.start_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="End Date (YYYY-MM-DD):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.end_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.end_var, width=30).grid(row=5, column=1, pady=5)
        
        ttk.Label(frame, text="Annual Premium (PKR):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.premium_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.premium_var, width=30).grid(row=6, column=1, pady=5)
        
        ttk.Button(frame, text="Save", command=self.save).grid(row=7, column=0, columnspan=2, pady=15)
    
    def save(self):
        success, msg = self.fleet_manager.add_insurance(
            self.car_var.get(),
            self.provider_var.get(),
            self.policy_var.get(),
            self.coverage_var.get(),
            self.start_var.get(),
            self.end_var.get(),
            self.premium_var.get()
        )
        messagebox.showinfo("Result", msg)
        if success:
            self.callback()
            self.destroy()
