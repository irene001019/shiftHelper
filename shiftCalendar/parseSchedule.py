import pdfplumber
from extract_dataformat import *
from utils import *
from dateCalculation import *

pdf_path = "PCL Schedule June 16-30.pdf"
index = 1
overall_schedule = []
year = 2025
month = 6


with pdfplumber.open(pdf_path) as pdf:
    page= pdf.pages[0]
    text = page.extract_text()
    for line in text.split("\n")[9:37]:
        list = extract_schedule(line)
        if list:
            overall_schedule.append(parse_weekly_row(list))
        else:
            overall_schedule.append(["empty"])
        
    #fill the date, if reach empty week+1
    week = -2
    for list in overall_schedule:
        day_in_week = 0
        for data in list:
            if data == "empty":
                week += 1
                continue
            elif data == "":
                day_in_week += 1 
                continue
            else :
                data['date'] = calculate_date(year, month, week,day_in_week).date().strftime('%Y-%m-%d')
                data['start_time'] = convert_to_24h(data['start_time'])
                if data['end_time'] == 'close':
                    data['end_time'] = get_close_time(day_in_week)
                else:
                    data['end_time'] = convert_to_24h(data['end_time'])
                
            print(f"Line {index}: {data}")
            day_in_week += 1
        index +=1