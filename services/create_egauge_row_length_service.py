import time
from typing import List
from helpers.egauge_data_handler import string_formatter

def create_egauge_row_length_service(list_length: int) -> str:
    """
    Generate a single InfluxDB line protocol metric for the length of a list.
    Example output: egauge_row_length length=88 1725678912000000000
    """
    measurement = string_formatter("egauge_row", context="measurement")
    field_value = str(list_length)
    timestamp_ns = int(time.time() * 1_000_000_000)  # current time in nanoseconds

    lp_line = f"{measurement} length={field_value} {timestamp_ns}"

    return lp_line
