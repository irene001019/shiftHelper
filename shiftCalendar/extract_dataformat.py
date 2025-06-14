import re
from dateCalculation import calculate_date



TARGET_NAMES = ["Sophia", "Anchen", "Yen", "Emily", "Karmen", "Man-lin", "Alizey", "Dani"]  
name_pattern = '|'.join(re.escape(name) for name in TARGET_NAMES)
schedule_pattern = re.compile(rf"(?P<name>{name_pattern})\s+(?P<start_time>\d{{1,2}}(?::\d{{2}})?)-(?P<end_time>close|\d{{1,2}}(?::\d{{2}})?)(?:\s+(?P<close_duty>\d+))?(?:\s+\((?P<duty>[A-Z])\))?")
# overall_schedule = []  #4 weeks, 7 days a week, start from sunday
days_in_week = ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

year = 2025
month = 6


def extract_person(text, target_name, week):
    results = []
    day_in_week= 0 ; # 0-Sun, 1-Mon, 2-Tue, 3-Wed, 4-Thu, 5-Fri, 6-Sat

    for match in schedule_pattern.finditer(text):
        data = match.groupdict()
        if data['name'] != target_name:
            day_in_week+1
            continue
        result = {
            'name': data['name'],
            'date' : calculate_date(year, month, week,day_in_week),
            'day_in_week' : days_in_week[day_in_week],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'close_duty': int(data['close_duty']) if data['close_duty'] else None,
            'duty': data['duty'] if data['duty'] else None,
        }
        day_in_week+1
        results.append(result)
        # overall_schedule.append(result)
    
    return results

#for grouping the lines
def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

