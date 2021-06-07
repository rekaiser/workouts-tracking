from typing import Iterable


def record_list_to_string(record: Iterable):
    record_string_list = []
    for value in record:
        if isinstance(value, str):
            record_string_list.append(f"'{value}'")
        else:
            record_string_list.append(f"{value}")
    entry_string = ", ".join(record_string_list)
    return entry_string


def columns_list_to_string(columns: Iterable[str]):
    columns_string = ", ".join(columns)
    return columns_string
