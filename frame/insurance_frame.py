import tkinter as tk
from tkinter import ttk, messagebox
from ui.dialogs.insurance_dialog import AddInsuranceDialog


class InsuranceFrame(ttk.Frame):
    def __init__(self, parent, fleet_manager, app):
        super().__init__(parent)
        self.fleet_manager = fleet_manager
        self.app = app
        self.create_widgets()
        self.refresh_alerts()
    
    def create_widgets(self):
        header = ttk.Label(self, text="Insurance Tracking", font=("Arial", 16, "bold"))
        header.pack(pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add Insurance", command=self.add_insurance).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Records", command=self.view_records).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Check Expiry", command=self.check_expiry).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Back", command=lambda: self.app.show_frame("MainMenu")).pack(side=tk.LEFT, padx=5)
        
        alert_label = ttk.Label(self, text="Expiry Alerts", font=("Arial", 12, "bold"))
        alert_label.pack(pady=10)
        
        alert_frame = ttk.Frame(self)
        alert_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.alert_text = tk.Text(alert_frame, height=15, width=80, state=tk.DISABLED)
        self.alert_text.pack(fill=tk.BOTH, expand=True)
    
    def add_insurance(self):
        AddInsuranceDialog(self.master, self.fleet_manager, self.refresh_alerts)
    
    def refresh_alerts(self):
        self.alert_text.config(state=tk.NORMAL)
        self.alert_text.delete("1.0", tk.END)
        self.alert_text.insert(tk.END, "Use 'Check Expiry' to see alerts for a specific date.")
        self.alert_text.config(state=tk.DISABLED)
    
    def check_expiry(self):
        ExpiryWindow(self.master, self.fleet_manager, self.refresh_alerts)
    
    def view_records(self):
        records = self.fleet_manager.get_insurance_records()
        RecordsWindow(self.master, records)


class ExpiryWindow(tk.Toplevel):
    def __init__(self, parent, fleet_manager, callback):
        super().__init__(parent)
        self.title("Check Expiry")
        self.geometry("400x150")
        self.fleet_manager = fleet_manager
        self.callback = callback
        
        ttk.Label(self, text="Enter today's date (YYYY-MM-DD):").pack(pady=10)
        self.date_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.date_var, width=20).pack(pady=5)
        
        def check():
            date_str = self.date_var.get()
            alerts, error = self.fleet_manager.check_insurance_expiry(date_str)
            if error:
                messagebox.showerror("Error", error)
            else:
                AlertsDisplayWindow(self, alerts)
        
        ttk.Button(self, text="Check", command=check).pack(pady=10)


class AlertsDisplayWindow(tk.Toplevel):
    def __init__(self, parent, alerts):
        super().__init__(parent)
        self.title("Insurance Alerts")
        self.geometry("700x400")
        
        text = tk.Text(self, height=20, width=80, state=tk.DISABLED)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.config(state=tk.NORMAL)
        if not alerts:
            text.insert(tk.END, "All insurance policies are valid.")
        else:
            for alert in alerts:
                status_icon = "[EXPIRED]" if alert['status'] == "EXPIRED" else "[EXPIRING]"
                text.insert(tk.END, f"{status_icon} {alert['car_label']} | {alert['provider']} | {alert['days_left']} days | Expires: {alert['end_date']}\n")
        text.config(state=tk.DISABLED)


class RecordsWindow(tk.Toplevel):
    def __init__(self, parent, records):
        super().__init__(parent)
        self.title("Insurance Records")
        self.geometry("900x400")
        
        tree = ttk.Treeview(self, columns=("ID", "Car", "Provider", "Policy", "Coverage", "Start", "End", "Premium"), height=15)
        tree.column("#0", width=0, stretch=tk.NO)
        for col in [("ID", 30), ("Car", 30), ("Provider", 80), ("Policy", 100), ("Coverage", 100), ("Start", 80), ("End", 80), ("Premium", 80)]:
            tree.column(col[0], anchor=tk.W, width=col[1])
            tree.heading(col[0], text=col[0], anchor=tk.W)
        
        for record in records:
            tree.insert("", "end", values=(record['id'], record['car_id'], record['provider'], record['policy_number'], record['coverage_type'], record['start_date'], record['end_date'], f"{record['premium']:.2f}"))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
