import tkinter as tk
from tkinter import ttk, messagebox
from utils import input_valid_date


class AddFuelDialog(tk.Toplevel):
    def __init__(self, parent, fleet_manager, callback):
        super().__init__(parent)
        self.title("Log Fuel Trip")
        self.geometry("400x250")
        self.fleet_manager = fleet_manager
        self.callback = callback
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Car selection
        ttk.Label(frame, text="Car ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.car_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.car_var, width=30).grid(row=0, column=1, pady=5)
        
        # Distance
        ttk.Label(frame, text="Distance (km):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.distance_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.distance_var, width=30).grid(row=1, column=1, pady=5)
        
        # Fuel price
        ttk.Label(frame, text="Fuel Price (PKR/L):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.price_var, width=30).grid(row=2, column=1, pady=5)
        
        # Date
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.date_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Button(frame, text="Save", command=self.save).grid(row=4, column=0, columnspan=2, pady=15)
    
    def save(self):
        success, msg, summary = self.fleet_manager.log_fuel(
            self.car_var.get(),
            self.distance_var.get(),
            self.price_var.get(),
            self.date_var.get()
        )
        
        if success:
            details = f"Distance: {summary['distance']} km\nFuel: {summary['fuel_used']} L\nCost: PKR {summary['cost']}"
            messagebox.showinfo("Result", msg + "\n\n" + details)
            self.callback()
            self.destroy()
        else:
            messagebox.showerror("Error", msg)
