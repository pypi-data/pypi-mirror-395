from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class GroupLesson:
    subject: Optional[str] = None
    teacher: Optional[str] = None
    room: Optional[str] = None

@dataclass
class Lesson:
    time: str
    groups: Dict[str, GroupLesson] = field(default_factory=dict)

@dataclass
class Day:
    name: str
    lessons: List[Lesson] = field(default_factory=list)

@dataclass
class Schedule:
    program: str
    days: List[Day] = field(default_factory=list)
