from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Type

from itertools import groupby
from operator import attrgetter
from ..Parser.FieldSelector import FieldSelector
from ..Data.ScheduleEntry import ScheduleEntry

from enum import Enum

class CollectionType(Enum):
    SET = 1
    LIST = 2
    
def filter_by(selector: FieldSelector, *scheduleEntries: ScheduleEntry):
    return set(filter(lambda s: selector.action(selector.value, getattr(s, selector.name)), scheduleEntries))

def concurent_filter(schedule, filter_by, selectors):
    filtered_sets = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        future_to_filter = {executor.submit(filter_by, selector, *schedule.copy()) for selector in selectors}
        for future in as_completed(future_to_filter):
            try:
                filtered_entries = future.result()
            except Exception as exc:
                print('%r generated an exception' % (exc))
            else:
                filtered_sets.append(filtered_entries)

    return filtered_sets

def group(collection, attr_name):
    key_func = attrgetter(attr_name)
    return [list(v) for l,v in groupby(sorted(collection, key=lambda x: key_func(x)), lambda x: key_func(x))]

def name_and_value(entry, attrs: str|tuple[str]):
    #if type(attrs) == str:
    #  return attrs, getattr(entry, attrs)
    #elif type(attrs) == tuple:
      return attrs, tuple(getattr(entry, attr) for attr in attrs)

def validated(clz:Type, select:str|tuple[str]):
    #if type(select) == str:
    #  return select if select in vars(clz)["__annotations__"] else None
    #elif type(select) == tuple:
      return tuple(s for s in select if s in vars(clz)["__annotations__"])

def map_to_names_values(clz:Type, entries, *, select:str|tuple[str], nthreads=4):
    values: list[tuple] = list()
    validated_select = validated(clz, select)
    selector = validated_select if validated_select else tuple(vars(clz)["__annotations__"].keys())
    with ProcessPoolExecutor(max_workers=nthreads) as executor:
      for entry in entries:
        future_distinct = {executor.submit(name_and_value, entry, selector)}
        for future in as_completed(future_distinct):
          try:
            values.append(future.result())
          except Exception as exc:
            print('%r generated an exception' % (exc))

    return values

def reduce_to_name_values(maps: list[tuple], collection:CollectionType=CollectionType.SET):
    reduced = {}
    for k, v in maps:
        if collection == CollectionType.SET:
            reduced.setdefault(k, set()).add(v)
        elif collection == CollectionType.LIST:
            reduced.setdefault(k, list()).append(v)
    return reduced