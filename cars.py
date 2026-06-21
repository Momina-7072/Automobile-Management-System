from file_manager import (
    cars_file, read_file, overwrite_file,
    append_to_file, generate_id
)
from utils import is_number


def get_car_by_id(car_id):
    """Returns car record or None"""
    records = read_file(cars_file)
    for r in records:
        if len(r) == 8 and r[0].strip() == car_id:
            return r
    return None


def get_all_cars():
    """Returns list of valid car records"""
    records = read_file(cars_file)
    return [r for r in records if len(r) == 8 and r[0].strip().isdigit()]


def add_vehicle(make, model, year, color, plate, mileage, efficiency):
    """
    Add car and return (success: bool, message: str, car_id: str or None)
    No input() or print() calls
    """
    if not make or not model or not year or not plate:
        return False, "Required fields missing", None

    if not is_number(year):
        return False, "Year must be numeric", None

    if not mileage:
        mileage = "0"

    if not is_number(mileage):
        return False, "Mileage must be numeric", None

    if not is_number(efficiency):
        return False, "Efficiency must be numeric", None

    car_id = generate_id(cars_file)
    record = [car_id, make, model, year, color, plate, mileage, efficiency]
    append_to_file(cars_file, record)
    return True, f"Car added successfully", car_id


def update_car(car_id, make="", model="", color="", plate="", mileage="", efficiency=""):
    """Update car fields (empty string = don't change)"""
    car = get_car_by_id(car_id)
    if not car:
        return False, "Car not found"

    if make:
        car[1] = make
    if model:
        car[2] = model
    if color:
        car[4] = color
    if plate:
        car[5] = plate
    if mileage and is_number(mileage):
        car[6] = mileage
    if efficiency and is_number(efficiency):
        car[7] = efficiency

    records = read_file(cars_file)
    updated = [car if r[0].strip() == car_id else r for r in records]
    overwrite_file(cars_file, updated)
    return True, "Car updated successfully"


def delete_car(car_id):
    """Delete car by ID"""
    car = get_car_by_id(car_id)
    if not car:
        return False, "Car not found"

    records = read_file(cars_file)
    updated = [r for r in records if r[0].strip() != car_id]
    overwrite_file(cars_file, updated)
    return True, "Car deleted"


def search_cars(keyword):
    """Search cars by keyword, return matching records"""
    keyword = keyword.lower()
    records = read_file(cars_file)
    found = []

    for r in records:
        if len(r) == 8 and r[0].strip().isdigit():
            if (
                keyword in r[1].lower()
                or keyword in r[2].lower()
                or keyword in r[4].lower()
                or keyword in r[5].lower()
            ):
                found.append(r)

    return found
