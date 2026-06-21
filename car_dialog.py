import tkinter as tk
from tkinter import ttk, messagebox


class AddCarDialog(tk.Toplevel):
    def __init__(self, parent, fleet_manager, callback):
        super().__init__(parent)
        self.title("Add Car")
        self.geometry("400x350")
        self.fleet_manager = fleet_manager
        self.callback = callback
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Make:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.make_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.make_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.model_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Year:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.year_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.year_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="Color:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.color_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="License Plate:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.plate_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.plate_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="Mileage (km):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.mileage_var = tk.StringVar(value="0")
        ttk.Entry(frame, textvariable=self.mileage_var, width=30).grid(row=5, column=1, pady=5)
        
        ttk.Label(frame, text="Fuel Efficiency (km/L):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.efficiency_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.efficiency_var, width=30).grid(row=6, column=1, pady=5)
        
        ttk.Button(frame, text="Save", command=self.save).grid(row=7, column=0, columnspan=2, pady=15)
    
    def save(self):
        success, msg, car_id = self.fleet_manager.add_car(
            self.make_var.get(),
            self.model_var.get(),
            self.year_var.get(),
            self.color_var.get(),
            self.plate_var.get(),
            self.mileage_var.get(),
            self.efficiency_var.get()
        )
        messagebox.showinfo("Result", msg)
        if success:
            self.callback()
            self.destroy()


class UpdateCarDialog(tk.Toplevel):
    def __init__(self, parent, fleet_manager, car, callback):
        super().__init__(parent)
        self.title("Update Car")
        self.geometry("400x350")
        self.fleet_manager = fleet_manager
        self.car_id = car['id']
        self.callback = callback
        
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Make:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.make_var = tk.StringVar(value=car['make'])
        ttk.Entry(frame, textvariable=self.make_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Model:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=car['model'])
        ttk.Entry(frame, textvariable=self.model_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Color:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar(value=car['color'])
        ttk.Entry(frame, textvariable=self.color_var, width=30).grid(row=2, column=1, pady=5)
        
        ttk.Label(frame, text="License Plate:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.plate_var = tk.StringVar(value=car['plate'])
        ttk.Entry(frame, textvariable=self.plate_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="Mileage (km):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.mileage_var = tk.StringVar(value=str(car['mileage']))
        ttk.Entry(frame, textvariable=self.mileage_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="Fuel Efficiency (km/L):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.efficiency_var = tk.StringVar(value=str(car['efficiency']))
        ttk.Entry(frame, textvariable=self.efficiency_var, width=30).grid(row=5, column=1, pady=5)
        
        ttk.Button(frame, text="Update", command=self.update).grid(row=6, column=0, columnspan=2, pady=15)
    
    def update(self):
        success, msg = self.fleet_manager.update_car(
            self.car_id,
            make=self.make_var.get() or None,
            model=self.model_var.get() or None,
            color=self.color_var.get() or None,
            plate=self.plate_var.get() or None,
            mileage=self.mileage_var.get() or None,
            efficiency=self.efficiency_var.get() or None
        )
        messagebox.showinfo("Result", msg)
        if success:
            self.callback()
            self.destroy()
