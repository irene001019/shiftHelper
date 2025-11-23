from PyPDF2 import PdfReader
from .extract_dataformat import *
from .dateCalculation import *
from datetime import datetime


# pdf_path = "../PCL Schedule Nov 1-15"

# index = 1

def parse_schedule_pdf(pdf_path, year, month):

    if year ==None or month== None:
        now = datetime.now()
        year = now.year
        month = now.month

    reader = PdfReader(pdf_path)
    overall_schedule = [] #for formating
    #get the first page, extract the text
    page = reader.pages[0]
    text = page.extract_text()

    lines = text.split("\n")
    
    start_parsing = False
    # Find where the schedule starts
    # We look for the header row containing "Sunday" and "Monday"
    
    schedule_lines = []
    for line in lines:
        if "Sunday" in line and "Monday" in line:
            start_parsing = True
            continue # Skip the header line itself
            
        if start_parsing:
            # Stop if we hit the bottom of the page (e.g. "Book Offs" or footer)
            if "Book Offs" in line or "Calendar Templates" in line:
                break
            schedule_lines.append(line)

    # If we didn't find the header, fallback to all lines (or maybe just skip metadata)
    if not schedule_lines and not start_parsing:
         # Fallback: try to guess based on content if header is missing/unreadable
         # But for now, let's assume the header is there as per the image.
         schedule_lines = lines[10:] # Fallback to skipping top metadata if header not found

    for line in schedule_lines:
        blocks = extract_schedule(line)
        if blocks:
            overall_schedule.append(parse_weekly_row(blocks))
        else:
            # Check for date row (only digits and spaces, at least 3 numbers)
            # This acts as a week separator
            if re.match(r'^[\d\s]+$', line) and len(line.split()) > 2:
                 overall_schedule.append(["empty"])
                 continue

            # Check for empty line
            if not line.strip():
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
            else:
                target = calculate_date(year, month, week, day_in_week)
                if target is None:
                    # Skip invalid cells (like overflow from previous/next month)
                    day_in_week += 1
                    continue

                data['date'] = target.date().strftime('%Y-%m-%d')
                data['start_time'] = convert_to_24h(data['start_time'])
                if data['end_time'] == 'close':
                    data['end_time'] = get_close_time(day_in_week)
                else:
                    data['end_time'] = convert_to_24h(data['end_time'])

            day_in_week += 1
    return overall_schedule
