import file_manager as fm
from utils import is_number
from cars import get_car_by_id


def log_fuel(car_id, distance, fuel_price, date):
    """
    Log fuel trip. Returns (success: bool, message: str, summary: dict or None)
    """
    car = get_car_by_id(car_id)
    if not car:
        return False, "Car not found", None

    if not is_number(distance) or not is_number(fuel_price):
        return False, "Distance and fuel price must be numeric", None

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
    record = [log_id, car_id, date, str(distance), str(fuel_used), str(cost), str(fuel_price)]
    fm.append_to_file(fm.fuel_file, record)

    car[6] = str(round(float(car[6]) + distance, 2))
    all_cars = fm.read_file(fm.cars_file)
    updated = [car if r[0] == car_id else r for r in all_cars]
    fm.overwrite_file(fm.cars_file, updated)

    summary = {
        "distance": distance,
        "fuel_used": fuel_used,
        "cost": cost
    }
    return True, "Fuel logged successfully", summary


def get_fuel_logs(car_id=None):
    """Get fuel logs. If car_id=None, return all. Return list of records."""
    logs = fm.read_file(fm.fuel_file)
    if car_id is None:
        return logs
    return [r for r in logs if len(r) == 7 and r[1] == car_id]
