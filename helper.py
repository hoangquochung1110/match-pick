from contextlib import contextmanager
import time
from decimal import Decimal
from page_object import Goal


@contextmanager  # type: ignore
def calculate_execution_time():
    """Calculate the execution time of a function.
    Append result to file_name.
    Args:
        file_name (str): The name of the file where the result will be saved.
    """
    start_time = time.time()
    try:
        yield  # pass control to func
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")

def sort_by_minute(goal: Goal):
    """Sort goals by minutes. Handle stoppage time."""
    x = goal.minute
    if "+" in x:
        x, y = x.split("+")
        return Decimal(".".join([x, y]))
    else:
        return int(x)