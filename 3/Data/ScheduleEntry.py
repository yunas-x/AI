from dataclasses import dataclass
from datetime import date as dt
from datetime import time as tm

@dataclass(frozen=True)
class ScheduleEntry:
    subject_name: str
    date: dt
    time_start: tm
    time_end: tm
    teacher: str
    group: str
