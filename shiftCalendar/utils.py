import re
from extract_dataformat import *

#for grouping the lines
def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]



def get_nth_block(line: str, n: int):
    blocks = re.split(rf"\s{2,}", line.strip())
    if n < len(blocks):
        return blocks[n]
    return ""