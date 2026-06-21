from file_manager import (
    cars_file, maintenance_file, read_file,
    append_to_file, generate_id
)
from utils import is_number
from cars import get_car_by_id


def add_maintenance(car_id, service_type, description, date, cost, mileage_done, next_due):
    """Add maintenance record"""
    car = get_car_by_id(car_id)
    if not car:
        return False, "Car not found"

    if not is_number(cost) or not is_number(mileage_done) or not is_number(next_due):
        return False, "Cost, mileage, and next due must be numbers"

    log_id = generate_id(maintenance_file)
    record = [log_id, car_id, date, service_type, description, cost, mileage_done, next_due]
    append_to_file(maintenance_file, record)
    return True, f"Service record added. Next due at {next_due} km"


def get_maintenance_logs(car_id=None):
    """Get maintenance logs"""
    logs = read_file(maintenance_file)
    if car_id is None:
        return logs
    return [r for r in logs if len(r) == 8 and r[1] == car_id]


def get_maintenance_reminders():
    """Get cars needing service (within 500 km)"""
    cars = read_file(cars_file)
    logs = read_file(maintenance_file)

    reminders = []
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
                        "car_id": car[0],
                        "car_label": f"{car[1]} {car[2]}",
                        "service": log[3],
                        "status": status,
                        "remaining": remaining
                    })
    return reminders
