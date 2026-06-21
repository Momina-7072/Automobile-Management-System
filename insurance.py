from file_manager import (
    insurance_file, read_file,
    append_to_file, generate_id
)
from utils import is_number, parse_date
from cars import get_car_by_id


def add_insurance(car_id, provider, policy_number, coverage_type, start_date, end_date, premium):
    """Add insurance record"""
    car = get_car_by_id(car_id)
    if not car:
        return False, "Car not found"

    if not is_number(premium):
        return False, "Premium must be numeric"

    log_id = generate_id(insurance_file)
    record = [log_id, car_id, provider, policy_number, coverage_type, start_date, end_date, premium]
    append_to_file(insurance_file, record)
    return True, f"Insurance added"


def get_insurance_records(car_id=None):
    """Get insurance records"""
    logs = read_file(insurance_file)
    if car_id is None:
        return logs
    return [r for r in logs if len(r) == 8 and r[1] == car_id]


def check_insurance_expiry(today_str):
    """Check expired/expiring insurance. Returns list of alerts"""
    today = parse_date(today_str)
    if not today:
        return []

    logs = read_file(insurance_file)
    alerts = []

    for r in logs:
        if len(r) != 8:
            continue

        car = get_car_by_id(r[1])
        car_label = f"{car[1]} {car[2]}" if car else f"Car {r[1]}"

        end_date = parse_date(r[6])
        if not end_date:
            continue

        diff = (end_date - today).days

        if diff < 0:
            alerts.append({
                "status": "EXPIRED",
                "car": car_label,
                "provider": r[2],
                "date": r[6],
                "days": diff
            })
        elif diff <= 30:
            alerts.append({
                "status": "EXPIRING",
                "car": car_label,
                "provider": r[2],
                "date": r[6],
                "days": diff
            })

    return alerts
