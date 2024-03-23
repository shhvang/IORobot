import time

def get_readable_time(seconds: int) -> str:
    intervals = [(' days, ', 86400), ('h:', 3600), ('m:', 60), ('s', 1)]
    time_string = ''
    for name, count in intervals:
        value = seconds // count
        if value > 0:
            seconds -= value * count
            time_string += f'{value}{name}'

    return time_string
