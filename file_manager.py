SEPARATOR = " | "

cars_file       = "cars.txt"
fuel_file       = "fuel.txt"
maintenance_file = "maintenance.txt"
insurance_file  = "insurance.txt"


def read_file(filename):
    try:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        records = []
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(SEPARATOR)
                records.append(parts)
        return records
    except:
        return []


def overwrite_file(filename, records):
    file = open(filename, "w")
    for record in records:
        file.write(SEPARATOR.join(record) + "\n")
    file.close()


def append_to_file(filename, record):
    for field in record:
        if SEPARATOR in field:
            print(f"Error: Field value cannot contain '{SEPARATOR}'. Record not saved.")
            return
    file = open(filename, "a")
    file.write(SEPARATOR.join(record) + "\n")
    file.close()


def generate_id(filename):
    records = read_file(filename)
    if not records:
        return "1"
    max_id = 0
    for record in records:
        try:
            num = int(record[0])
            if num > max_id:
                max_id = num
        except:
            pass
    return str(max_id + 1)
