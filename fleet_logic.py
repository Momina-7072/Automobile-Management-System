"""
PURE BUSINESS LOGIC - No UI dependencies. No print statements.
This is what you wire into Tkinter later.
"""

import file_manager as fm
from utils import is_number, parse_date
from datetime import date as date_type


class FleetManager:
    """Core logic for the entire fleet system"""
    
    def __init__(self):
        pass
    
    # ===== CAR OPERATIONS =====
    
    def add_car(self, make, model, year, color, plate, mileage, efficiency):
        """Add a car. Returns (success, message, car_id)"""
        
        if not make or not model or not year or not plate:
            return False, "Required fields missing", None
        
        if not is_number(year):
            return False, "Year must be numeric", None
        
        if not is_number(mileage):
            return False, "Mileage must be numeric", None
        
        if not is_number(efficiency):
            return False, "Efficiency must be numeric", None
        
        car_id = fm.generate_id(fm.cars_file)
        record = [car_id, make, model, year, color, plate, mileage, efficiency]
        
        try:
            fm.append_to_file(fm.cars_file, record)
            return True, f"Car added successfully! ID: {car_id}", car_id
        except Exception as e:
            return False, f"Error saving car: {str(e)}", None
    
    def get_all_cars(self):
        """Get all cars as list of dicts"""
        records = fm.read_file(fm.cars_file)
        cars = []
        for r in records:
            if len(r) == 8 and r[0].strip().isdigit():
                cars.append({
                    'id': r[0],
                    'make': r[1],
                    'model': r[2],
                    'year': r[3],
                    'color': r[4],
                    'plate': r[5],
                    'mileage': float(r[6]),
                    'efficiency': float(r[7])
                })
        return cars
    
    def get_car(self, car_id):
        """Get single car or None"""
        r = self._get_car_raw(car_id)
        if not r:
            return None
        return {
            'id': r[0],
            'make': r[1],
            'model': r[2],
            'year': r[3],
            'color': r[4],
            'plate': r[5],
            'mileage': float(r[6]),
            'efficiency': float(r[7])
        }
    
    def _get_car_raw(self, car_id):
        """Internal: get raw record"""
        car_id = str(car_id).strip()  # Tkinter Treeview returns int for numeric values
        records = fm.read_file(fm.cars_file)
        for r in records:
            if len(r) == 8 and r[0].strip() == car_id:
                return r
        return None
    
    def update_car(self, car_id, make=None, model=None, color=None, plate=None, mileage=None, efficiency=None):
        """Update car. Returns (success, message)"""
        car_id = str(car_id).strip()
        
        car = self._get_car_raw(car_id)
        if not car:
            return False, "Car not found"
        
        if mileage is not None and not is_number(mileage):
            return False, "Mileage must be numeric"
        
        if efficiency is not None and not is_number(efficiency):
            return False, "Efficiency must be numeric"
        
        if make:
            car[1] = make
        if model:
            car[2] = model
        if color:
            car[4] = color
        if plate:
            car[5] = plate
        if mileage is not None:
            car[6] = str(mileage)
        if efficiency is not None:
            car[7] = str(efficiency)
        
        records = fm.read_file(fm.cars_file)
        updated = [car if r[0].strip() == car_id else r for r in records]
        
        try:
            fm.overwrite_file(fm.cars_file, updated)
            return True, "Car updated"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_car(self, car_id):
        """Delete car. Returns (success, message)"""
        car_id = str(car_id).strip()
        
        if not self._get_car_raw(car_id):
            return False, "Car not found"
        
        records = fm.read_file(fm.cars_file)
        updated = [r for r in records if r[0].strip() != car_id]
        
        try:
            fm.overwrite_file(fm.cars_file, updated)
            return True, "Car deleted"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def search_cars(self, keyword):
        """Search cars by keyword"""
        keyword = keyword.lower()
        records = fm.read_file(fm.cars_file)
        results = []
        
        for r in records:
            if len(r) == 8 and r[0].strip().isdigit():
                if (keyword in r[1].lower() or keyword in r[2].lower() 
                    or keyword in r[4].lower() or keyword in r[5].lower()):
                    results.append({
                        'id': r[0],
                        'make': r[1],
                        'model': r[2],
                        'year': r[3],
                        'color': r[4],
                        'plate': r[5],
                        'mileage': float(r[6]),
                        'efficiency': float(r[7])
                    })
        
        return results
    
    # ===== FUEL OPERATIONS =====
    
    def log_fuel(self, car_id, distance, fuel_price, date_str):
        """Log fuel trip. Returns (success, message, summary_dict)"""
        car_id = str(car_id).strip()
        
        car = self._get_car_raw(car_id)
        if not car:
            return False, "Car not found", None
        
        if not is_number(distance) or not is_number(fuel_price):
            return False, "Distance and price must be numeric", None
        
        distance = float(distance)
        fuel_price = float(fuel_price)
        efficiency = float(car[7])
        
        if efficiency <= 0:
            return False, "Invalid car efficiency", None
        
        fuel_used = distance / efficiency
        cost = fuel_used * fuel_price
        
        fuel_used = round(fuel_used, 2)
        cost = round(cost, 2)
        
        log_id = fm.generate_id(fm.fuel_file)
        record = [log_id, car_id, date_str, str(distance), str(fuel_used), str(cost), str(fuel_price)]
        
        try:
            fm.append_to_file(fm.fuel_file, record)
            
            # Update mileage
            car[6] = str(round(float(car[6]) + distance, 2))
            all_cars = fm.read_file(fm.cars_file)
            updated = [car if r[0] == car_id else r for r in all_cars]
            fm.overwrite_file(fm.cars_file, updated)
            
            summary = {
                'distance': distance,
                'fuel_used': fuel_used,
                'cost': cost
            }
            return True, "Fuel logged", summary
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def get_fuel_logs(self, car_id=None):
        """Get fuel logs. If car_id is None, return all"""
        logs = fm.read_file(fm.fuel_file)
        results = []
        
        for r in logs:
            if len(r) == 7:
                if car_id is None or r[1] == car_id:
                    results.append({
                        'id': r[0],
                        'car_id': r[1],
                        'date': r[2],
                        'distance': float(r[3]),
                        'fuel_used': float(r[4]),
                        'cost': float(r[5]),
                        'fuel_price': float(r[6])
                    })
        
        return results
    
    # ===== MAINTENANCE OPERATIONS =====
    
    def add_maintenance(self, car_id, service_type, description, date_str, cost, mileage_done, next_due):
        """Add maintenance record. Returns (success, message)"""
        
        car = self._get_car_raw(car_id)
        if not car:
            return False, "Car not found"
        
        if not is_number(cost) or not is_number(mileage_done) or not is_number(next_due):
            return False, "Cost, mileage, and next_due must be numeric"
        
        log_id = fm.generate_id(fm.maintenance_file)
        record = [log_id, car_id, date_str, service_type, description, cost, mileage_done, next_due]
        
        try:
            fm.append_to_file(fm.maintenance_file, record)
            return True, f"Service record added. Next due at {next_due} km"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_maintenance_logs(self, car_id=None):
        """Get maintenance logs"""
        logs = fm.read_file(fm.maintenance_file)
        results = []
        
        for r in logs:
            if len(r) == 8:
                if car_id is None or r[1] == car_id:
                    results.append({
                        'id': r[0],
                        'car_id': r[1],
                        'date': r[2],
                        'service_type': r[3],
                        'description': r[4],
                        'cost': float(r[5]),
                        'mileage_done': float(r[6]),
                        'next_due': float(r[7])
                    })
        
        return results
    
    def check_maintenance_reminders(self):
        """Check maintenance due. Returns list of reminders"""
        reminders = []
        cars = fm.read_file(fm.cars_file)
        logs = fm.read_file(fm.maintenance_file)
        
        if not cars or not logs:
            return reminders
        
        for log in logs:
            if len(log) != 8:
                continue
            
            for car in cars:
                if len(car) == 8 and car[0] == log[1]:
                    try:
                        remaining = float(log[7]) - float(car[6])
                    except:
                        continue
                    
                    if remaining <= 500:
                        status = "OVERDUE" if remaining < 0 else f"{round(remaining)} km left"
                        reminders.append({
                            'car_id': car[0],
                            'car_label': f"{car[1]} {car[2]} ({car[3]})",
                            'service': log[3],
                            'status': status,
                            'is_overdue': remaining < 0
                        })
        
        return reminders
    
    # ===== INSURANCE OPERATIONS =====
    
    def add_insurance(self, car_id, provider, policy_number, coverage_type, start_date, end_date, premium):
        """Add insurance. Returns (success, message)"""
        
        car = self._get_car_raw(car_id)
        if not car:
            return False, "Car not found"
        
        if not is_number(premium):
            return False, "Premium must be numeric"
        
        log_id = fm.generate_id(fm.insurance_file)
        record = [log_id, car_id, provider, policy_number, coverage_type, start_date, end_date, premium]
        
        try:
            fm.append_to_file(fm.insurance_file, record)
            return True, f"Insurance added"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_insurance_records(self, car_id=None):
        """Get insurance records"""
        logs = fm.read_file(fm.insurance_file)
        results = []
        
        for r in logs:
            if len(r) == 8:
                if car_id is None or r[1] == car_id:
                    results.append({
                        'id': r[0],
                        'car_id': r[1],
                        'provider': r[2],
                        'policy_number': r[3],
                        'coverage_type': r[4],
                        'start_date': r[5],
                        'end_date': r[6],
                        'premium': float(r[7])
                    })
        
        return results
    
    def check_insurance_expiry(self, today_str):
        """Check insurance expiry. Returns (alerts_list, error_if_any)"""
        
        today = parse_date(today_str)
        if not today:
            return [], "Invalid date format"
        
        logs = fm.read_file(fm.insurance_file)
        alerts = []
        
        for r in logs:
            if len(r) != 8:
                continue
            
            car = self._get_car_raw(r[1])
            car_label = f"{car[1]} {car[2]} ({car[3]})" if car else f"Car {r[1]}"
            
            end_date = parse_date(r[6])
            if not end_date:
                continue
            
            diff = (end_date - today).days
            
            if diff < 0:
                alerts.append({
                    'car_label': car_label,
                    'provider': r[2],
                    'status': 'EXPIRED',
                    'days_left': diff,
                    'end_date': r[6]
                })
            elif diff <= 30:
                alerts.append({
                    'car_label': car_label,
                    'provider': r[2],
                    'status': 'EXPIRING',
                    'days_left': diff,
                    'end_date': r[6]
                })
        
        return alerts, None
    
    # ===== COMPARISON =====
    
    def get_car_stats(self, car_id):
        """Get stats for a car"""
        fuel_logs = [r for r in fm.read_file(fm.fuel_file) if len(r) == 7 and r[1] == car_id]
        maint_logs = [r for r in fm.read_file(fm.maintenance_file) if len(r) == 8 and r[1] == car_id]
        
        total_fuel_cost = sum(float(r[5]) for r in fuel_logs)
        total_maint_cost = sum(float(r[5]) for r in maint_logs)
        total_eff = sum(float(r[6]) for r in fuel_logs)
        
        avg_eff = round((total_eff / len(fuel_logs)) * 100) / 100 if fuel_logs else 0
        
        return {
            'fuel_cost': total_fuel_cost,
            'maint_cost': total_maint_cost,
            'avg_efficiency': avg_eff,
            'services_count': len(maint_logs)
        }
    
    def compare_cars(self, car_id1, car_id2):
        """Compare two cars. Returns (comparison_dict, error_if_any)"""
        
        car1 = self.get_car(car_id1)
        car2 = self.get_car(car_id2)
        
        if not car1 or not car2:
            return None, "One or both cars not found"
        
        stats1 = self.get_car_stats(car_id1)
        stats2 = self.get_car_stats(car_id2)
        
        return {
            'car1': car1,
            'car2': car2,
            'stats1': stats1,
            'stats2': stats2
        }, None
