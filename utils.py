from datetime import date as date_type


def pause():
    input("\nEnter to continue...")


def is_number(value):
    try:
        float(value)
        return True
    except:
        return False


def input_valid_date(prompt):
    while True:
        d = input(prompt).strip()
        try:
            y, m, day = map(int, d.split("-"))
            date_type(y, m, day)
            return d
        except:
            print("Enter date in YYYY-MM-DD format!")


def parse_date(date_str):
    try:
        parts = date_str.split("-")
        return date_type(int(parts[0]), int(parts[1]), int(parts[2]))
    except:
        return None
