from pprint import pprint
from datetime import datetime
from datetime import date as dt
from datetime import time as tm

from operator import eq, lt, gt, ne, le, ge

from .Data.ScheduleEntry import ScheduleEntry
from .Data.ScheduleList import schedule


from .Functionals.Functionals import CollectionType, concurent_filter, filter_by, map_to_names_values, reduce_to_name_values

from .Parser.FieldSelector import FieldSelector
from .Parser.QueryParser import QueryParser

def early_demo():
    # Early Demo bellow
    selectors = [FieldSelector[str]("subject_name", eq, "Интелектуальные_системы"), 
                 FieldSelector[str]("group", ne, "ПИ-20-1"), 
                 FieldSelector[str]("date", ne, dt(2023, 5, 20))]

    sets = concurent_filter(schedule, filter_by, selectors)
    print(set.intersection(*sets))

def get_time_diffs(times):
    diffs = [(datetime.combine(times[c+1][2], times[c+1][0]) - 
            datetime.combine(times[c][2],times[c][1])).seconds / 60
            for c in range(len(times) - 1)
            if times[c+1][1] != times[c][1] or times[c+1][0] != times[c][0]]
            
    return diffs

def get_time_dupes(elems):
    dupes = any(elems[c+1][1] != elems[c][1] or elems[c+1][0] != elems[c][0]
            for c in range(len(elems) - 1))
            
    return dupes

def smart_demo():
    ## Check if we can add
    date = "2023/05/20"
    time_start = "9:20"
    time_end = "11:00"
    teacher = "Мухин"
    group = "ПИ-20-2"
    subject_name = "Интелектуальные_системы"

    """
                        Можно поставить     Дубликаты -> окна        Фильтр
    date                    +                       +                  o
    time_start              +                       +                  o
    time_end                +                       +                  o
    teacher                 o                       o                  o
    group                   o                       o                  o
    subject_name            +                       o                  o
    """
    
    #query = f"date={date} and time_start>={time_start} and time_end<={time_end} and group={group} and subject_name<>{subject_name}"
    #query = f"date={date} and time_start>={time_start} and time_end<={time_end} and teacher={teacher} and subject_name<>{subject_name}"
    #query = f"date={date} and time_start>={time_start} and time_end<={time_end} and teacher={teacher} or! group={group} and subject_name<>{subject_name}"

    query = f"date={date} and teacher={teacher}"

    tokens = QueryParser.tokenize(query)
    parsed_tokens = QueryParser.parse(tokens)
    entries = QueryParser.process_expression(parsed_tokens, schedule=schedule)

    entries = sorted(list(entries), key=lambda e: e.time_start)
    pprint(entries)

    maps = map_to_names_values(ScheduleEntry, entries, select=("time_start", "time_end", 'date'), nthreads=4)
    reduced = reduce_to_name_values(maps, collection=CollectionType.LIST)

    times = reduced[('time_start', 'time_end', 'date')]
    pprint(times)

    dupes = get_time_dupes(times)
    pprint(f"{dupes=}")

    diffs = get_time_diffs(times)
    print(f"{diffs=}")

    print(f"gaps longer than 30 min: {any(x>30 for x in diffs)}")

def parsing_demo():
    
    ## Entries parsing
    ## group=БИ-20-1 or subject_name=Интелектуальные_системы
    query = input("Input our query: ")
    if query:
        tokens = QueryParser.tokenize(query)
        parsed_tokens = QueryParser.parse(tokens)
        entries = QueryParser.process_expression(parsed_tokens, schedule=schedule)
    else:
        entries = schedule
    pprint(entries)

    ## Map and Reduce
    ## subject_name, date
    field_selectors = tuple(f_sel.strip() for f_sel in input("Input fields to get: ").split(",") if f_sel)
    if not field_selectors:
        field_selectors = tuple(vars(ScheduleEntry)["__annotations__"].keys())

    maps = map_to_names_values(ScheduleEntry, entries, select=field_selectors, nthreads=4)
    filter_duplicates = input("Filter duplicates [y]: ").lower()
    if filter_duplicates == "y":
        reduced = reduce_to_name_values(maps, collection=CollectionType.SET)
    else:
        reduced = reduce_to_name_values(maps, collection=CollectionType.LIST)
    pprint(reduced)