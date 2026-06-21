from file_manager import fuel_file, maintenance_file, read_file
from cars import get_car_by_id


def get_comparison_stats(car_id):
    """Get stats for comparison"""
    fuel_logs = [r for r in read_file(fuel_file) if len(r) == 7 and r[1] == car_id]
    maint_logs = [r for r in read_file(maintenance_file) if len(r) == 8 and r[1] == car_id]

    total_fuel_cost = sum(float(r[5]) for r in fuel_logs) if fuel_logs else 0
    total_maint_cost = sum(float(r[5]) for r in maint_logs) if maint_logs else 0
    total_eff = sum(float(r[6]) for r in fuel_logs) if fuel_logs else 0

    avg_eff = round((total_eff / len(fuel_logs)) * 100) / 100 if fuel_logs else 0

    return {
        "fuel_cost": total_fuel_cost,
        "maint_cost": total_maint_cost,
        "avg_eff": avg_eff,
        "services": len(maint_logs)
    }


def compare_cars(car_id1, car_id2):
    """Compare two cars. Returns comparison dict or error"""
    car1 = get_car_by_id(car_id1)
    car2 = get_car_by_id(car_id2)

    if not car1 or not car2:
        return None

    stats1 = get_comparison_stats(car_id1)
    stats2 = get_comparison_stats(car_id2)

    return {
        "car1": {
            "id": car1[0],
            "make": car1[1],
            "model": car1[2],
            "year": car1[3],
            "color": car1[4],
            "plate": car1[5],
            "mileage": car1[6],
            "stats": stats1
        },
        "car2": {
            "id": car2[0],
            "make": car2[1],
            "model": car2[2],
            "year": car2[3],
            "color": car2[4],
            "plate": car2[5],
            "mileage": car2[6],
            "stats": stats2
        }
    }
