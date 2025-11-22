
from datetime import datetime

def derive_date(start_date):
    year, month = None, None
    if start_date:
        try:
            dt = datetime.strptime(start_date, "%Y-%m-%d")
            year = dt.year
            month = dt.month
        except ValueError:
            pass 
    
    if not year or not month:
            now = datetime.now()
            year = now.year
            month = now.month
    return year, month

print("Testing Date Derivation:")

# Test 1: Valid Start Date
y, m = derive_date("2025-11-01")
print(f"Input: 2025-11-01 -> Year: {y}, Month: {m} [{'✅' if y==2025 and m==11 else '❌'}]")

# Test 2: No Start Date (Should be current date)
y, m = derive_date(None)
now = datetime.now()
print(f"Input: None       -> Year: {y}, Month: {m} [{'✅' if y==now.year and m==now.month else '❌'}]")

# Test 3: Invalid Start Date (Should be current date)
y, m = derive_date("invalid-date")
print(f"Input: Invalid    -> Year: {y}, Month: {m} [{'✅' if y==now.year and m==now.month else '❌'}]")
