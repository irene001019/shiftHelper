import re
from dateCalculation import *

TARGET_NAMES = ["Sophia", "Anchen", "Yen", "Emily", "Karmen", "Man-lin", "Alizey", "Dani", "Ruby"]  
name_pattern = '|'.join(re.escape(name) for name in TARGET_NAMES)
schedule_pattern = re.compile(rf"(?P<name>{name_pattern})\s+(?P<start_time>\d{{1,2}}(?::\d{{2}})?)-(?P<end_time>close|\d{{1,2}}(?::\d{{2}})?)(?:\s+(?P<close_duty>\d+))?(?:\s+\((?P<duty>[A-Z])\))?")
full_schedule = []  #4 weeks, 7 days a week, start from sunday
days_in_week = ["Sunday","Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

year = 2025
month = 6

#split by names
def parse_weekly_row(line, week:int):
    entries = [] #full schedule
    day_in_week= 0 ; # 0-Sun, 1-Mon, 2-Tue, 3-Wed, 4-Thu, 5-Fri, 6-Sat
    for match in schedule_pattern.finditer(line):
        data = match.groupdict()
        
        result = {
            'name': data['name'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'close_duty': int(data['close_duty']) if data['close_duty'] else None,
            'duty': data['duty'] if data['duty'] else None,
        }
        entries.append(result)
    
    if not entries:
        return [{} for _ in range(7)]

    
    # make sure it's 7 days
    if len(entries) < 7:
        first_entry = entries[0]
        remaining_entries = entries[1:]
        blanks_needed = 7 - len(entries)
        entries = [first_entry].extend([""] * blanks_needed + remaining_entries)

     #Add actual date
    for day_in_week, entry in enumerate(entries[:7]):
        entry['start_time'] = convert_to_24h(entry['start_time'])
                        
        if entry['end_time'] == 'close':
            entry['end_time'] = get_close_time(entry['day_in_week'])
        else:
            entry['end_time'] = convert_to_24h(entry['end_time'])

        entry['day_in_week'] = day_in_week
        entry['date'] = calculate_date(year, month, week,day_in_week).date().strftime('%Y-%m-%d')

    return entries[:7]


def extract_person(full_schedule, target_name):
    result = []
    for week in full_schedule:
        for day in week:
            if day.get("name") == target_name:
                result.append(day)
    return result
    # results = []
    # day_in_week= 0 ; # 0-Sun, 1-Mon, 2-Tue, 3-Wed, 4-Thu, 5-Fri, 6-Sat

    # for match in schedule_pattern.finditer(text):
    #     data = match.groupdict()
    #     if data['name'] != target_name or day_in_week==1:
    #         day_in_week += 1
    #         continue

    #     day_in_week += 1
    #     result = {
    #         'name': data['name'],
    #         'date' : calculate_date(year, month, week,day_in_week).date().strftime('%Y-%m-%d'),
    #         'day_in_week' : day_in_week,
    #         'start_time': data['start_time'],
    #         'end_time': data['end_time'],
    #         'close_duty': int(data['close_duty']) if data['close_duty'] else None,
    #         'duty': data['duty'] if data['duty'] else None,
    #     }
    #     # day_in_week += 1
    #     results.append(result)
    #     # overall_schedule.append(result)
    


