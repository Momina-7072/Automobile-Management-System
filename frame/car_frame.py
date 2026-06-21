import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.car_dialog import AddCarDialog, UpdateCarDialog


class CarFrame(ttk.Frame):
    def __init__(self, parent, fleet_manager, app):
        super().__init__(parent)
        self.fleet_manager = fleet_manager
        self.app = app
        self.create_widgets()
        self.refresh_list()
    
    def create_widgets(self):
        header = ttk.Label(self, text="Car Management", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Add Car", command=self.add_car).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_car).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_car).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=lambda: self.app.show_frame("MainMenu")).pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=10)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.search_cars())
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Make", "Model", "Year", "Color", "Plate", "Mileage", "Efficiency"), height=15)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", anchor=tk.W, width=30)
        self.tree.column("Make", anchor=tk.W, width=80)
        self.tree.column("Model", anchor=tk.W, width=80)
        self.tree.column("Year", anchor=tk.W, width=50)
        self.tree.column("Color", anchor=tk.W, width=60)
        self.tree.column("Plate", anchor=tk.W, width=70)
        self.tree.column("Mileage", anchor=tk.W, width=70)
        self.tree.column("Efficiency", anchor=tk.W, width=70)
        
        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor=tk.W)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
    
    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        cars = self.fleet_manager.get_all_cars()
        for car in cars:
            self.tree.insert("", "end", values=(car['id'], car['make'], car['model'], car['year'], car['color'], car['plate'], f"{car['mileage']:.1f}", f"{car['efficiency']:.2f}"))
    
    def search_cars(self):
        keyword = self.search_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not keyword:
            self.refresh_list()
            return
        cars = self.fleet_manager.search_cars(keyword)
        for car in cars:
            self.tree.insert("", "end", values=(car['id'], car['make'], car['model'], car['year'], car['color'], car['plate'], f"{car['mileage']:.1f}", f"{car['efficiency']:.2f}"))
    
    def add_car(self):
        AddCarDialog(self.master, self.fleet_manager, self.refresh_list)
    
    def update_car(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a car to update.")
            return
        car_id = str(self.tree.item(selection[0])['values'][0])
        car = self.fleet_manager.get_car(car_id)
        if car:
            UpdateCarDialog(self.master, self.fleet_manager, car, self.refresh_list)
    
    def delete_car(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a car to delete.")
            return
        car_id = str(self.tree.item(selection[0])['values'][0])
        car = self.fleet_manager.get_car(car_id)
        if messagebox.askyesno("Confirm", f"Delete {car['make']} {car['model']}?"):
            success, msg = self.fleet_manager.delete_car(car_id)
            messagebox.showinfo("Result", msg)
            if success:
                self.refresh_list()
