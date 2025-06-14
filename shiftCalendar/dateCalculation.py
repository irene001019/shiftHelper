from datetime import datetime, timedelta
# Note:  week starts with Sunday (day_in_week=0)

def calculate_date(year: int, month: int, week: int, day_in_week: int):
    #first day of the month
    first_day = datetime(year, month, 1)
    # weekday() returns 0 = Monday, so we convert to 0 = Sunday format
    first_weekday = (first_day.weekday() + 1) % 7  # 0 = Sunday, 6 = Saturday

    # days to shift from June 1 to the [week, day]
    days_offset = (week * 7 + day_in_week) - first_weekday
    target_date = first_day + timedelta(days=days_offset)
    if target_date.month != month:
        return None  # Invalid date cell (e.g. overflow into May or July)
    return target_date
