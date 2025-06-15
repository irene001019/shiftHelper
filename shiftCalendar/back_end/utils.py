
#convert 2d array to the flat list+dict
def flatten_schedule(overall_schedule):
    flatList = []
    for week in overall_schedule:
        if week == ["empty"]:
            continue
        for day in week:
            if day != "" and isinstance(day, dict):
                flatList.append(day)
    return flatList
