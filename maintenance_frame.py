import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.maintenance_dialog import AddMaintenanceDialog


class MaintenanceFrame(ttk.Frame):
    def __init__(self, parent, fleet_manager, app):
        super().__init__(parent)
        self.fleet_manager = fleet_manager
        self.app = app
        self.create_widgets()
        self.refresh_reminders()
    
    def create_widgets(self):
        header = ttk.Label(self, text="Maintenance Tracker", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add Service", command=self.add_service).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Logs", command=self.view_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Check Reminders", command=self.refresh_reminders).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=lambda: self.app.show_frame("MainMenu")).pack(side=tk.LEFT, padx=5)
        
        # Reminders section
        reminder_label = ttk.Label(self, text="Service Reminders (Due within 500 km)", font=("Arial", 12, "bold"))
        reminder_label.pack(pady=10)
        
        reminder_frame = ttk.Frame(self)
        reminder_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.reminder_text = tk.Text(reminder_frame, height=10, width=80, state=tk.DISABLED)
        self.reminder_text.pack(fill=tk.BOTH, expand=True)
    
    def add_service(self):
        AddMaintenanceDialog(self.master, self.fleet_manager, self.refresh_reminders)
    
    def refresh_reminders(self):
        reminders = self.fleet_manager.check_maintenance_reminders()
        self.reminder_text.config(state=tk.NORMAL)
        self.reminder_text.delete("1.0", tk.END)
        
        if not reminders:
            self.reminder_text.insert(tk.END, "All services are up to date.")
        else:
            for reminder in reminders:
                status_text = f"[!] {reminder['car_label']} | {reminder['service']} | {reminder['status']}\n"
                self.reminder_text.insert(tk.END, status_text)
        
        self.reminder_text.config(state=tk.DISABLED)
    
    def view_logs(self):
        logs = self.fleet_manager.get_maintenance_logs()
        LogsWindow(self.master, logs)


class LogsWindow(tk.Toplevel):
    def __init__(self, parent, logs):
        super().__init__(parent)
        self.title("Maintenance Logs")
        self.geometry("900x400")
        
        tree = ttk.Treeview(self, columns=("ID", "Car", "Date", "Service", "Description", "Cost", "Mileage", "Next Due"), height=15)
        tree.column("#0", width=0, stretch=tk.NO)
        for col in [("ID", 30), ("Car", 30), ("Date", 80), ("Service", 100), ("Description", 120), ("Cost", 70), ("Mileage", 80), ("Next Due", 80)]:
            tree.column(col[0], anchor=tk.W, width=col[1])
            tree.heading(col[0], text=col[0], anchor=tk.W)
        
        for log in logs:
            tree.insert("", "end", values=(log['id'], log['car_id'], log['date'], log['service_type'], log['description'], f"{log['cost']:.2f}", f"{log['mileage_done']:.1f}", f"{log['next_due']:.1f}"))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
