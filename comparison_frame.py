import tkinter as tk
from tkinter import ttk, messagebox


class ComparisonFrame(ttk.Frame):
    def __init__(self, parent, fleet_manager, app):
        super().__init__(parent)
        self.fleet_manager = fleet_manager
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        header = ttk.Label(self, text="Car Comparison", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Car 1 ID:").pack(side=tk.LEFT, padx=5)
        self.car1_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.car1_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(input_frame, text="Car 2 ID:").pack(side=tk.LEFT, padx=5)
        self.car2_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.car2_var, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="Compare", command=self.compare).pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text="Back", command=lambda: self.app.show_frame("MainMenu")).pack(pady=5)
        
        self.result_text = tk.Text(self, height=20, width=100, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def compare(self):
        car_id1 = self.car1_var.get().strip()
        car_id2 = self.car2_var.get().strip()
        
        if not car_id1 or not car_id2:
            messagebox.showwarning("Warning", "Enter both car IDs.")
            return
        
        result, error = self.fleet_manager.compare_cars(car_id1, car_id2)
        
        if error:
            messagebox.showerror("Error", error)
            return
        
        car1 = result['car1']
        car2 = result['car2']
        stats1 = result['stats1']
        stats2 = result['stats2']
        
        label1 = f"{car1['make']} {car1['model']} ({car1['year']})"
        label2 = f"{car2['make']} {car2['model']} ({car2['year']})"
        
        text = f"{'Attribute':<30} {label1:<40} {label2:<40}\n"
        text += "-" * 110 + "\n"
        text += f"{'Plate':<30} {car1['plate']:<40} {car2['plate']:<40}\n"
        text += f"{'Color':<30} {car1['color']:<40} {car2['color']:<40}\n"
        text += f"{'Mileage (km)':<30} {car1['mileage']:<40} {car2['mileage']:<40}\n"
        text += f"{'Avg Efficiency (km/L)':<30} {stats1['avg_efficiency']:<40} {stats2['avg_efficiency']:<40}\n"
        text += f"{'Fuel Cost (PKR)':<30} {stats1['fuel_cost']:<40.2f} {stats2['fuel_cost']:<40.2f}\n"
        text += f"{'Maintenance Cost (PKR)':<30} {stats1['maint_cost']:<40.2f} {stats2['maint_cost']:<40.2f}\n"
        text += f"{'Total Cost (PKR)':<30} {stats1['fuel_cost'] + stats1['maint_cost']:<40.2f} {stats2['fuel_cost'] + stats2['maint_cost']:<40.2f}\n"
        text += f"{'Services Done':<30} {stats1['services_count']:<40} {stats2['services_count']:<40}\n"
        text += "\nVerdict:\n"
        
        if stats1['avg_efficiency'] > stats2['avg_efficiency']:
            text += f"  Better efficiency: {label1}\n"
        elif stats2['avg_efficiency'] > stats1['avg_efficiency']:
            text += f"  Better efficiency: {label2}\n"
        else:
            text += "  Efficiency: Tie\n"
        
        total1 = stats1['fuel_cost'] + stats1['maint_cost']
        total2 = stats2['fuel_cost'] + stats2['maint_cost']
        
        if total1 < total2:
            text += f"  Lower total cost: {label1}\n"
        elif total2 < total1:
            text += f"  Lower total cost: {label2}\n"
        else:
            text += "  Total cost: Tie\n"
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)
