from typing import Callable
from operator import eq, lt, gt, ne, le, ge

from queue import LifoQueue
from ..Parser.FieldSelector import FieldSelector
from ..Functionals.Functionals import filter_by

from ..Data.ScheduleEntry import ScheduleEntry
from ..Data.ScheduleList import ScheduleList
from .TypeAdapter import TypeAdapter

class QueryParser:
    # Формальная грамматика языка: <{name of attribute}{=|!=|>|<}{value}(\space{or!|and|or}\space{name of attribute}{=|!=|>|<}{value}))*>
    # Приоритет операций по нисходящей: or! (логическое или с макс. приоритетом), and (логическое и), or (логическое или без приоритета)
    # Можно добавить преобразование or! в or при переводе в польскую нотацию
    # Можно добавить вывод других операторов сравнения
    # Интерпретатор работает по принципу автомата с магазином
    # a=b or c=d and e=f or! g=h and j=k
    
    _conjunctions: dict[str, Callable] = {  "and!": set.intersection,
                                            "or!": set.union,
                                            "and": set.intersection,
                                            "or": set.union,}

    _conjunction_list: list[str] = ["and!",
                                    "or!",
                                    "and",
                                    "or",]

    _operations: dict[str, Callable] = {">=": le,
                                        "<=": ge,
                                        "=": eq,
                                        "!=": ne,
                                        "<>": ne,
                                        ">": lt,
                                        "<": gt,}

    @staticmethod
    def tokenize(query: str) -> list[str]:
        return [s.strip() for s in query.split(" ") if not s.isspace()]

    @staticmethod
    def _get_reversed_stack(stack: LifoQueue[str]):
        reversed: LifoQueue[str] = LifoQueue()
        while not stack.empty():
            e = stack.get()
            reversed.put(e)
        return reversed

    @staticmethod
    def parse(tokens: list[str]):
        stack: LifoQueue[str] = LifoQueue()
        conjunctions: list[str] = list()

        for e in tokens:
            if e not in QueryParser._conjunctions:
                stack.put(e)
            else:
                # If needs to pop
                if conjunctions and QueryParser._conjunction_list.index(e) >= QueryParser._conjunction_list.index(conjunctions[-1]):
                    while conjunctions and QueryParser._conjunction_list.index(e) >= QueryParser._conjunction_list.index(conjunctions[-1]):
                        o = conjunctions.pop()
                        stack.put(o)

                conjunctions.append(e)

            # Get remained
        while conjunctions:
            o = conjunctions.pop()
            stack.put(o)

        return QueryParser._get_reversed_stack(stack)

    @staticmethod
    def process_expression(stack: LifoQueue[str], schedule: ScheduleList):
        set_stack: LifoQueue[set[ScheduleEntry]] = LifoQueue()
        while not stack.empty():
            exp = stack.get()
            if exp in QueryParser._conjunctions:
                filtered = QueryParser._conjunctions[exp](
                    set_stack.get(),
                    set_stack.get()
                )
                set_stack.put(filtered)

            else:
                for op in QueryParser._operations:
                    if op in exp:
                        name, value = exp.split(op)
                        break
                if name:
                    value = TypeAdapter().adapt(name, value, ScheduleEntry)
                    selector = FieldSelector(name, QueryParser._operations[op], value)
                    filtered = filter_by(selector, *schedule)
                    set_stack.put(filtered)

        return set_stack.get()