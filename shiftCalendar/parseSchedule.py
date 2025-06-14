import pdfplumber
from extract_dataformat import *
from utils import *
from dateCalculation import *

pdf_path = "PCL Schedule June 16-30.pdf"
date_index = 0
groupSize = 6 #have to change it to 5 later since we dont have 5:30 person
overall_schedule = []

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        lines = text.split("\n")

        for week_index, group_lines in enumerate(chunks(lines[9:37] , groupSize),0):
            week_schedule = []
            for line in group_lines:
                parsed_row = parse_weekly_row(line, week_index)
                week_schedule.append(parsed_row)
            overall_schedule.append(week_schedule)
                # print(f"\tinfo: {parse_weekly_row(line,week_index)}")
                # datas = extract_person(line, "Man-lin", group_index)
                # if datas:
                #     overall_schedule.extend(datas)
                #     for data in overall_schedule:
                #         data['start_time'] = convert_to_24h(data['start_time'])
                        
                #         if data['end_time'] == 'close':
                #             data['end_time'] = get_close_time(data['day_in_week'])
                #         else:
                #             data['end_time'] = convert_to_24h(data['end_time'])

print(overall_schedule,f"\n\tTotal working days :{len(overall_schedule)}")

