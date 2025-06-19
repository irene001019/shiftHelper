from ics import Calendar, Event
from datetime import datetime
from pytz import timezone
import json
import os

class ScheduleManager:
    def __init__(self, raw_schedule):
        self.overall_schedule = raw_schedule
        self.flat_schedule = self._flatten_schedule()

    #convert 2d array to the flat list+dict
    def _flatten_schedule(self):
        flat = []
        for week in self.overall_schedule:
            if week == ["empty"]:
                continue
            for day in week:
                if isinstance(day, dict):
                    flat.append(day)
                elif isinstance(day, list):
                    for entry in day:
                        if isinstance(entry, dict):
                            flat.append(entry)
        return flat

    def export_to_json(self, file_path="output_schedule.json", filter_fn=None):
        """
        Export flat schedule to a JSON file.

        Parameters:
        - file_path: str = where to save the file
        - filter_fn: callable = optional function to filter schedule entries
        """
        if filter_fn is not None:
            data = list(filter(filter_fn, self.flat_schedule))
        else:
            data = self.flat_schedule

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Schedule exported to {os.path.abspath(file_path)}")


    def export_to_ics(self, file_path="schedule.ics", filter_fn=None):
        """
        Export flat schedule to a ics file.

        Parameters:
        - file_path: str = where to save the file
        - filter_fn: callable = optional function to filter schedule entries
        """
        cal = Calendar()
        tz = timezone("America/Winnipeg")

        if filter_fn is not None:
            data = list(filter(filter_fn, self.flat_schedule))
        else:
            data = self.flat_schedule

        for entry in data:
            # Parse datetime
            date_str = entry.get("date")
            start_str = entry.get("start_time")
            end_str = entry.get("end_time")
            name = entry.get("name")

            if not date_str or not start_str or not end_str:
                continue  # skip incomplete records

            try:
                start_dt_naive = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
                end_dt_naive = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")

                start_dt = tz.localize(start_dt_naive)
                end_dt = tz.localize(end_dt_naive)
            except Exception as e:
                print(f"⚠️ Error parsing time for {entry}: {e}")
                continue

            event = Event()
            event.name = f"{entry.get('name')}'s Work {entry.get('close_duty') or ''}({(entry.get('duty')) or ''})"
            event.begin = start_dt
            event.end = end_dt

            cal.events.add(event)

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(cal)
        print(f"📅 .ics file exported to {os.path.abspath(file_path)}")


    def get_by_person(self, name):
        return [entry for entry in self.flat_schedule if entry.get("name") == name]

    def get_by_date(self, date_str):
        return [entry for entry in self.flat_schedule if entry.get("date") == date_str]

    def get_all_people(self):
        return sorted(set(entry["name"] for entry in self.flat_schedule if "name" in entry))

    def get_all_dates(self):
        return sorted(set(entry["date"] for entry in self.flat_schedule if "date" in entry))

    def __repr__(self):
        return f"<ScheduleManager with {len(self.flat_schedule)} entries>"
