from models.schedule import Schedule, Day, Lesson, GroupLesson

class ScheduleParser:
    def parse(self, sheet_name, raw_data):
        groups = raw_data[1][1:]
        schedule = Schedule(program=sheet_name)

        current_day = None
        i = 2
        while i < len(raw_data):
            row = raw_data[i]
            if not any(row):
                i += 1
                continue

            first = row[0].strip()
            if first in ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]:
                current_day = Day(name=first)
                schedule.days.append(current_day)
                i += 1
                continue

            if ":" in first:
                subjects = raw_data[i][1:]
                teachers = raw_data[i+1][1:] if i+1 < len(raw_data) else []
                rooms = raw_data[i+2][1:] if i+2 < len(raw_data) else []
                lesson = Lesson(time=first)
                for idx, g in enumerate(groups):
                    subj, tchr, room = subjects[idx], teachers[idx], rooms[idx]
                    if subj or tchr or room:
                        lesson.groups[g] = GroupLesson(subj, tchr, room)
                current_day.lessons.append(lesson)
                i += 3
            else:
                i += 1
        return schedule
