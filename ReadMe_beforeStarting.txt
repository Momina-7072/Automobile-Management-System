Last Modified: 10:25AM 5/31/26 
Author: Momina Ahmad ( 553880)
this file explains how to run project,structure of all files, basic functionality of all modules and everything you need to know before testing our system.

How to Run our system

1. Extract the project folder
2. Open the folder in VS Code or any Python IDE(i used VS CODE)
3. Make sure Python is installed on your computer
4. Run the file named "main_gui.py"
5. The main menu of the Automobile Management System will open

FILE STRUCTURE
main_gui.py
  - Starts the app and controls screen switching.

fleet_logic.py
  - All logic and calculations. No GUI code here.

cars.py / fuel.py / maintenance.py / insurance.py / comparison.py
  - Helper functions for each section (add, update, delete, search).

file_manager.py
  - Reads and writes data to .txt files.

utils.py
  - Small helper functions (e.g. check if a value is a number, parse dates).

cars.txt
  - Stores all car records. Created automatically when you add a car.

ui/frames/
  - One file per screen (Cars, Fuel, Maintenance, Insurance, Comparison).

ui/dialogs/
  - Pop-up forms for entering data (Add Car, Log Fuel, etc.).

__init__.py files
  - Empty files that tell Python to treat folders as packages. Required.


DATA FILES
The app auto-creates these files when data is saved:
  cars.txt, fuel.txt, maintenance.txt, insurance.txt


Notes
1. All modules can be accessed from main menu.
2. The project contains 23 files because a modular design approach was followed. Each major feature and GUI component was implemented in a separate file making the code easier to manage
3.Follow the buttons and on-screen options to perform different operations
4.Tkinter was selected because it is lightweight, easy to deploy, and suitable for rapid desktop application development. The project's primary focus was implementing vehicle management functionality rather than exploring advanced GUI frameworks


Funtinality of each module
This project consists of five main modules:

1. Car Management
   
   Add new vehicles.
   Update vehicle information.
   Delete vehicle records.
   View all registered vehicles.

2. Fuel Tracking
   
    Record fuel expenses and trips.
    Monitor fuel consumption.
    Keep track of fuel costs.

3. Maintenance Management
   
    Add vehicle service records.
    Store maintenance history.
    Track upcoming service requirements.

4. Insurance Management
    Store insurance details of vehicles.
    Record policy information.
    Track insurance validity and coverage.
   
   
5. Vehicle Comparison
   
    Compare vehicles based on stored data.
    View performance and cost-related information.

