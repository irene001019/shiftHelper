from collections import defaultdict

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

    def get_by_person(self, name):
        return [entry for entry in self.flat_schedule if entry.get("name") == name]

    def get_by_date(self, date_str):
        return [entry for entry in self.flat_schedule if entry.get("date") == date_str]

    def get_all_people(self):
        return sorted(set(entry["name"] for entry in self.flat_schedule if "name" in entry))

    def get_all_dates(self):
        return sorted(set(entry["date"] for entry in self.flat_schedule if "date" in entry))
