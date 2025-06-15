from datetime import datetime, timedelta

def calculate_date(year: int, month: int, week: int, day_in_week: int):
    #first day of the month
    first_day = datetime(year, month, 8)
    
    # weekday() returns 0 = Monday, so we convert to 0 = Sunday format
    weekday = (first_day.weekday() + 1) % 7  # 0 = Sunday, 6 = Saturday
    
    days_offset = (week * 7 + day_in_week) - weekday
    target_date = first_day + timedelta(days=days_offset)

    if target_date.month != month:
        return None  # Invalid date cell (e.g. overflow into May or July)
    return target_date

#close time convert
def get_close_time(day_in_week):
    if day_in_week == 1:
        return None  # monday closed
    elif day_in_week in [0, 2, 3, 4]:
        return "20:00"
    elif day_in_week in [5, 6]:
        return "21:00"

#12hr to 24hr convert
def convert_to_24h(time_str, is_close=False):
    if time_str is None:
        return None  

    if ':' not in time_str:
        time_str += ":00"
    hour, minute = map(int, time_str.split(":"))

    if is_close or hour < 11:  # assume any shift start time before 11:00 are pm
        hour += 12
    return f"{hour:02}:{minute:02}"
