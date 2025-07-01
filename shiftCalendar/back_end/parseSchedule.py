import pdfplumber
from extract_dataformat import *
from dateCalculation import *

# pdf_path = "../PCL Schedule June 16-30.pdf"
# index = 1

def parse_schedule_pdf(pdf_path, year, month):

    with pdfplumber.open(pdf_path) as pdf:
        overall_schedule = [] #for formating
        #get the first page, extract the text
        page= pdf.pages[0]
        text = page.extract_text()

        lines = text.split("\n")
       
        for line in lines[9:37]:
            blocks = extract_schedule(line)
            if blocks:
                overall_schedule.append(parse_weekly_row(blocks))
            else:
                overall_schedule.append(["empty"])
            
        #fill the date, if reach empty week+1
        week = -1
        for row in overall_schedule:
            day_in_week = 0
            for data in row:
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
                    
                day_in_week += 1
    return overall_schedule
