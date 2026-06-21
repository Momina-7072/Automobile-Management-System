import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.fuel_dialog import AddFuelDialog


class FuelFrame(ttk.Frame):
    def __init__(self, parent, fleet_manager, app):
        super().__init__(parent)
        self.fleet_manager = fleet_manager
        self.app = app
        self.create_widgets()
        self.refresh_list()
    
    def create_widgets(self):
        header = ttk.Label(self, text="Fuel Tracker", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add Trip", command=self.add_trip).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=lambda: self.app.show_frame("MainMenu")).pack(side=tk.LEFT, padx=5)
        
        filter_frame = ttk.Frame(self)
        filter_frame.pack(pady=10)
        ttk.Label(filter_frame, text="Car ID:").pack(side=tk.LEFT, padx=5)
        self.car_id_var = tk.StringVar(value="All")
        self.car_id_var.trace_add("write", lambda *args: self.refresh_list())
        ttk.Entry(filter_frame, textvariable=self.car_id_var, width=10).pack(side=tk.LEFT, padx=5)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Car", "Date", "Distance", "Fuel", "Cost", "Price/L"), height=15)
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in [("ID", 30), ("Car", 30), ("Date", 80), ("Distance", 80), ("Fuel", 80), ("Cost", 80), ("Price/L", 80)]:
            self.tree.column(col[0], anchor=tk.W, width=col[1])
            self.tree.heading(col[0], text=col[0], anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        car_filter = self.car_id_var.get()
        car_id = None if car_filter == "All" else car_filter
        logs = self.fleet_manager.get_fuel_logs(car_id)
        for log in logs:
            self.tree.insert("", "end", values=(log['id'], log['car_id'], log['date'], f"{log['distance']:.2f}", f"{log['fuel_used']:.2f}", f"{log['cost']:.2f}", f"{log['fuel_price']:.2f}"))
    
    def add_trip(self):
        AddFuelDialog(self.master, self.fleet_manager, self.refresh_list)
