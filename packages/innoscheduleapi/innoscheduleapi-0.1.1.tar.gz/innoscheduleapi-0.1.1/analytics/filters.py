def filter_by_teacher(schedule, name):
    for day in schedule.days:
        for lesson in day.lessons:
            for group, data in lesson.groups.items():
                if name.lower() in (data.teacher or "").lower():
                    yield day.name, lesson.time, group, data
