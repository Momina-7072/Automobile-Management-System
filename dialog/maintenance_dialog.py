import tkinter as tk
from tkinter import ttk, messagebox


class AddMaintenanceDialog(tk.Toplevel):
    def __init__(self, parent, fleet_manager, callback):
        super().__init__(parent)
        self.title("Add Service Record")
        self.geometry("450x400")
        self.fleet_manager = fleet_manager
        self.callback = callback
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Car ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.car_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.car_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Service Type:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.service_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.service_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Description/Notes:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.desc_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.date_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="Cost (PKR):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.cost_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.cost_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="Mileage at Service (km):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.mileage_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.mileage_var, width=30).grid(row=5, column=1, pady=5)
        
        ttk.Label(frame, text="Next Service Due (km):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.next_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.next_var, width=30).grid(row=6, column=1, pady=5)
        
        ttk.Button(frame, text="Save", command=self.save).grid(row=7, column=0, columnspan=2, pady=15)
    
    def save(self):
        success, msg = self.fleet_manager.add_maintenance(
            self.car_var.get(),
            self.service_var.get(),
            self.desc_var.get(),
            self.date_var.get(),
            self.cost_var.get(),
            self.mileage_var.get(),
            self.next_var.get()
        )
        messagebox.showinfo("Result", msg)
        if success:
            self.callback()
            self.destroy()
