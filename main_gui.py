"""
Main GUI Application Entry Point
"""

import tkinter as tk
from tkinter import ttk, messagebox
from fleet_logic import FleetManager
from ui.frames.car_frame import CarFrame
from ui.frames.fuel_frame import FuelFrame
from ui.frames.maintenance_frame import MaintenanceFrame
from ui.frames.insurance_frame import InsuranceFrame
from ui.frames.comparison_frame import ComparisonFrame


class FleetManagementApp(tk.Tk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        self.fleet_manager = FleetManager()
        self.title("Automobile Management System")
        self.geometry("900x600")
        
        # Create frames dictionary
        self.frames = {}
        self.current_frame = None
        
        # Create container
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.container = container
        
        # Create menu
        self.create_menu()
        
        # Show main menu frame
        self.show_frame("MainMenu")
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.quit)
        
        navigate_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Navigate", menu=navigate_menu)
        navigate_menu.add_command(label="Cars", command=lambda: self.show_frame("Cars"))
        navigate_menu.add_command(label="Fuel", command=lambda: self.show_frame("Fuel"))
        navigate_menu.add_command(label="Maintenance", command=lambda: self.show_frame("Maintenance"))
        navigate_menu.add_command(label="Insurance", command=lambda: self.show_frame("Insurance"))
        navigate_menu.add_command(label="Comparison", command=lambda: self.show_frame("Comparison"))
        navigate_menu.add_command(label="Home", command=lambda: self.show_frame("MainMenu"))
    
    def show_frame(self, frame_name):
        """Switch to a frame"""
        
        # Destroy old frame
        if self.current_frame:
            self.current_frame.destroy()
        
        # Create new frame
        if frame_name == "MainMenu":
            frame = MainMenuFrame(self.container, self)
        elif frame_name == "Cars":
            frame = CarFrame(self.container, self.fleet_manager, self)
        elif frame_name == "Fuel":
            frame = FuelFrame(self.container, self.fleet_manager, self)
        elif frame_name == "Maintenance":
            frame = MaintenanceFrame(self.container, self.fleet_manager, self)
        elif frame_name == "Insurance":
            frame = InsuranceFrame(self.container, self.fleet_manager, self)
        elif frame_name == "Comparison":
            frame = ComparisonFrame(self.container, self.fleet_manager, self)
        else:
            return
        
        self.current_frame = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()


class MainMenuFrame(ttk.Frame):
    """Home/Main menu frame"""
    
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = ttk.Label(self, text="Automobile Management System", 
                         font=("Arial", 20, "bold"))
        title.pack(pady=20)
        
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        
        buttons = [
            ("Car Management", "Cars"),
            ("Fuel Tracker", "Fuel"),
            ("Maintenance Tracker", "Maintenance"),
            ("Insurance Tracking", "Insurance"),
            ("Compare Cars", "Comparison")
        ]
        
        for text, frame_name in buttons:
            btn = ttk.Button(button_frame, text=text, 
                           command=lambda fn=frame_name: self.app.show_frame(fn),
                           width=25)
            btn.pack(pady=10)
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="Exit", command=self.app.quit, width=25)
        exit_btn.pack(pady=10)


if __name__ == "__main__":
    app = FleetManagementApp()
    app.mainloop()
