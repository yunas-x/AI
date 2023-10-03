from datetime import date as dt
from datetime import time as tm
from datetime import datetime
from typing import Any, Type

class TypeAdapter:
    def __init__(self, format_date: str="%Y/%m/%d", format_time: str="%H:%M"):
        self.format_date = format_date
        self.format_time = format_time

    def adapt(self, name: str, value: Any, clz: Type):
        t = vars(clz)["__annotations__"][name]
        if type(value) is t:
            return value
        if t is dt:
            return datetime.strptime(value, self.format_date).date()
        if t is tm:
            return datetime.strptime(value, self.format_time).time()