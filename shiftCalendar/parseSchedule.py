import pdfplumber
from extract_dataformat import *

pdf_path = "PCL Schedule June 16-30.pdf"
date_index = 0
groupSize = 6 #have to change it to 5 later since we dont have 5:30 person
overall_schedule = []

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        lines = text.split("\n")
        for group_index, group_lines in enumerate(chunks(lines[9:37] , groupSize),0):

            for line in group_lines:
                # print(line)
                # print("✅ line",date_index,": ",line)
                # date_index+=1
                datas = extract_person(line, "Man-lin", group_index)
                if datas:
                    overall_schedule.extend(datas)
                
          
print(overall_schedule,f"\n\tTotal working days :{len(overall_schedule)}")

# print("total working days: "  ,date_index)
