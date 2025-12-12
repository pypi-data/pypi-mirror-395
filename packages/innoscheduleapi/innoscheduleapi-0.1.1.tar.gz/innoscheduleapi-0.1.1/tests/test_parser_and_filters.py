from analytics.filters import filter_by_teacher
from core.parser import ScheduleParser
from models.schedule import Day, GroupLesson, Lesson, Schedule


def test_schedule_parser_builds_days_and_lessons():
    raw_data = [
        ["", ""],
        ["", "G1", "G2"],
        ["MONDAY", "", ""],
        ["09:00", "Math", "Physics"],
        ["", "Dr. Smith", "Prof. Doe"],
        ["", "101", "202"],
        ["", ""],
        ["TUESDAY", "", ""],
        ["10:30", "Algorithms", ""],
        ["", "Dr. Smith", ""],
        ["", "303", ""],
    ]

    parser = ScheduleParser()
    schedule = parser.parse("B21", raw_data)

    assert schedule.program == "B21"
    assert [d.name for d in schedule.days] == ["MONDAY", "TUESDAY"]
    monday = schedule.days[0]
    assert monday.lessons[0].time == "09:00"
    assert monday.lessons[0].groups["G1"].subject == "Math"
    assert monday.lessons[0].groups["G2"].teacher == "Prof. Doe"

    tuesday = schedule.days[1]
    assert tuesday.lessons[0].groups["G1"].room == "303"
    assert "G2" not in tuesday.lessons[0].groups


def test_filter_by_teacher_matches_case_insensitive():
    lesson = Lesson(
        time="12:00",
        groups={"G1": GroupLesson(subject="ML", teacher="Jane Roe", room="101")},
    )
    schedule = Schedule(program="B21", days=[Day(name="MONDAY", lessons=[lesson])])

    results = list(filter_by_teacher(schedule, "jane"))

    assert results == [("MONDAY", "12:00", "G1", lesson.groups["G1"])]
