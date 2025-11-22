
from schedule_manager import ScheduleManager
import json

# Mock data with a missing date entry
mock_schedule = [
    [{"date": "2023-10-01", "name": "Alice", "start_time": "09:00", "end_time": "17:00"}],
    [{"date": "2023-10-05", "name": "Alice", "start_time": "09:00", "end_time": "17:00"}],
    [{"name": "Alice", "start_time": "09:00", "end_time": "17:00"}], # Missing date
]

mgr = ScheduleManager(mock_schedule)

print("Testing No Filter:")
mgr.export_to_json("test_all.json")
with open("test_all.json") as f:
    data = json.load(f)
    print(f"Count: {len(data)}")

print("\nTesting Start Date 2023-10-05 (Should not crash):")
try:
    mgr.export_to_json("test_start.json", start_date="2023-10-05")
    with open("test_start.json") as f:
        data = json.load(f)
        print(f"Count: {len(data)}")
        print([e.get("date") for e in data])
except Exception as e:
    print(f"FAILED: {e}")
