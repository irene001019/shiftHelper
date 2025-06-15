import re
from extract_dataformat import *
# #split by names
# def split_by_names(line):
#     blocks = []
#     for match in schedule_pattern.finditer(line):
#         data = match.groupdict()
#         blocks.append(data['name'])
 
#     if not blocks:
#         # if no matches found, return 7 empty slots
#         return [""] * 7
    
#     # make sure it's 7 days
#     if len(blocks) < 7:
#         first_block = blocks[0]
#         remaining_blocks = blocks[1:]
#         blanks_needed = 7 - len(blocks)
#         blocks = [first_block] + [""] * blanks_needed + remaining_blocks
#     return blocks[:7]


#for grouping the lines
def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]



def get_nth_block(line: str, n: int):
    blocks = re.split(rf"\s{2,}", line.strip())
    if n < len(blocks):
        return blocks[n]
    return ""