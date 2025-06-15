import re
from dateCalculation import *

TARGET_NAMES = ["Sophia", "Anchen", "Yen", "Emily", "Karmen", "Man-lin", "Alizey", "Dani", "Ruby"]  
name_pattern = '|'.join(re.escape(name) for name in TARGET_NAMES)
schedule_pattern = re.compile(rf"(?P<name>{name_pattern})\s+(?P<start_time>\d{{1,2}}(?::\d{{2}})?)-(?P<end_time>close|\d{{1,2}}(?::\d{{2}})?)(?:\s+(?P<close_duty>\d+))?(?:\s+\((?P<duty>[A-Z])\))?")



# make it 7 days
def parse_weekly_row(list):
    if len(list) < 7:
        
        first_item = list[0]
        remaining_list = list[1:]
        blanks_needed = 7 - len(list)
        list = [first_item]+([""] * blanks_needed + remaining_list)
    return list

def extract_schedule(line):
    results = []

    for match in schedule_pattern.finditer(line):
        data = match.groupdict()
      
        result = {
            'name': data['name'],
            'start_time': data['start_time'],
            'end_time': data['end_time'],
            'close_duty': int(data['close_duty']) if data['close_duty'] else None,
            'duty': data['duty'] if data['duty'] else None,
        }
        results.append(result)
    return results


