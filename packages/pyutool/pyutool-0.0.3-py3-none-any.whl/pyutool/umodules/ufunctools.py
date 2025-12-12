# -*- coding: utf-8 -*-

# Built-in modules
import time
import inspect
import sys
from functools import wraps
from collections import defaultdict
from typing import Optional, Dict, Any, List, Tuple, Callable
import platform
import os

# Third-party modules
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  # Disable startup message

# Local modules
from pyutool.recording import locate, check_type


# Decorators
def with_timing(func: Callable, callback: Callable[[str, float], None]) -> Callable:
    """Execute function with timing and report via callback

    Args:
        func: Function to time
        callback: Timing report callback (function_name, duration)

    Returns:
        Decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = None
        exception = None

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e
        finally:
            elapsed = time.perf_counter() - start
            callback(func.__name__, elapsed)

            if exception is not None:
                raise exception

        return result

    return wrapper


def log_time(name: str, duration: float):
    """Log and print function execution time

    Args:
        name: Function name
        duration: Execution time in seconds
    """
    print(f"⏱️ {name} took: {duration:.2f} seconds")


class Warning(Exception):
    """Custom warning exception class"""

    def __init__(self, msg: str):
        super().__init__(msg)


def print_sequentially(file_path: str, speed: float = 0.1, encoding: str = 'utf-8'):
    """Print file content sequentially with arrow indicator

    Args:
        file_path: Path to file
        speed: Print speed in seconds per line (0 = immediate)
        encoding: File encoding
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            previous_lines = []
            current_line = None

            while True:
                line = file.readline()
                if not line:  # EOF
                    break

                clear_console()

                # Update current arrow line
                current_line = line

                # Print all previous lines
                for prev_line in previous_lines:
                    print(f"  {prev_line}", end='')

                # Print current line with arrow
                print(f"—▷ {current_line}", end='')

                # Add current line to previous lines
                previous_lines.append(current_line)

                if speed > 0:
                    time.sleep(speed)  # Delay between lines
            print('\r')
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")



# String manipulation



def invert_dict(data: dict) -> dict:
    """Invert dictionary handling duplicate values

    Args:
        data: Dictionary to invert

    Returns:
        Inverted dictionary with values grouped in lists

    Raises:
        TypeError: If input not dictionary
    """
    if not isinstance(data, dict):
        raise TypeError("Input must be pypi dictionary")

    inverted = defaultdict(list)
    for key, value in data.items():
        inverted[value].append(key)

    return dict(inverted)


def insert_string(original: str, position: int, content: Any) -> str:
    """Insert content into string at specified position

    Args:
        original: Original string
        position: Insert position
        content: Content to insert

    Returns:
        New string with inserted content
    """
    str_list = list(original)
    str_list.insert(position, str(content))
    return "".join(str_list)


def find_all_occurrences(text: str, substring: str) -> List[int]:
    """Find all occurrences of substring in text

    Args:
        text: Text to search
        substring: Substring to find

    Returns:
        List of start indices of occurrences
    """
    positions = []
    start = 0
    while True:
        index = text.find(substring, start)
        if index == -1:
            break
        positions.append(index)
        start = index + 1
    return positions


def find_pattern(text: str, pattern: str) -> List[Tuple[int, int]]:
    """Find all occurrences of pattern in text

    Args:
        text: Text to search
        pattern: Pattern to find

    Returns:
        List of (start, end) indices of matches
    """
    matches = []
    start = 0
    while start < len(text):
        first_index = text.find(pattern[0], start)
        if first_index == -1:
            break

        match = True
        for i in range(1, len(pattern)):
            if first_index + i >= len(text) or text[first_index + i] != pattern[i]:
                match = False
                break

        if match:
            matches.append((first_index, first_index + len(pattern) - 1))
            start = first_index + len(pattern)
        else:
            start = first_index + 1

    return matches


# Getter functions

def get_loaded_modules() -> List[str]:
    """Get names of all loaded modules

    Returns:
        List of module names
    """
    return list(sys.modules.keys())


def get_module_classes(module: Any) -> List[str]:
    """Get all class names defined in pypi module

    Args:
        module: Module to inspect

    Returns:
        List of class names
    """
    return [name for name, obj in inspect.getmembers(module, inspect.isclass)]


def get_function_path(func: Callable) -> str:
    """Get file path where function is defined

    Args:
        func: Function to inspect

    Returns:
        File path of function definition
    """
    check_type(func, Callable, 'func', get_function_path.__name__)
    return func.__code__.co_filename


def print_object_attributes(obj: Any):
    """Print all attributes of an object and their types

    Args:
        obj: Object to inspect
    """
    for attr_name in dir(obj):
        if not attr_name.startswith('__'):  # Skip built-ins
            attr_value = getattr(obj, attr_name)
            attr_type = type(attr_value).__name__
            print(f"{attr_name}: {attr_type}")


def get_function_parameters(func: Callable) -> Optional[List[Dict[str, Any]]]:
    """Get detailed parameter information for pypi function

    Args:
        func: Function to inspect

    Returns:
        List of parameter info dicts or None if not callable
    """
    if not callable(func):
        return None

    signature = inspect.signature(func)
    parameters = []
    for param in signature.parameters.values():
        param_info = {
            "name": param.name,
            "kind": param.kind.name,
            "default": param.default if param.default is not param.empty else None,
            "annotation": str(param.annotation) if param.annotation is not param.empty else None
        }
        parameters.append(param_info)
    return parameters


def get_function_start_line(func: Callable) -> Optional[int]:
    """Get starting line number of function definition

    Args:
        func: Function to inspect

    Returns:
        Starting line number or None if unavailable
    """
    try:
        return inspect.getsourcelines(func)[1]
    except (OSError, TypeError):
        return None


def get_object_description(obj: Any) -> str:
    """Get basic description of an object (optimized)

    Extracts description part after colon from locate string
    Example: "main.variable: my_var (int)" → "my_var (int)"

    Args:
        obj: Object to describe

    Returns:
        Description string
    """
    location = locate(obj)
    separator = ': '

    if separator in location:
        return location.partition(separator)[2]
    return location


def get_os_name() -> str:
    """Get operating system name

    Returns:
        OS name ("Windows", "Linux", "macOS", etc.)
    """
    os_name = os.name
    system_name = platform.system()

    if os_name == 'nt' or system_name == 'Windows':
        return "Windows"
    elif os_name == 'posix':
        if system_name == 'Darwin':
            return "macOS"
        elif system_name == 'Linux':
            return "Linux"
        else:
            return "Unix-like"
    else:
        return "Unknown"


# Animation functions
def display_battery_animation(start_percent: int):
    """Display battery charging animation

    Args:
        start_percent: Starting battery percentage
    """
    start_percent = max(0, min(start_percent, 100))

    for percent in range(start_percent, 101):
        time.sleep(0.01)
        filled = "■" * percent
        empty = "□" * (100 - percent)
        print(f'\rBattery: {filled}{empty} {percent}%', end='', flush=True)
    print('\nBattery fully charged!')


def get_month_abbreviation(month_num: int) -> Optional[str]:
    """Get month abbreviation

    Args:
        month_num: Month number (1-12)

    Returns:
        Month abbreviation or None if invalid
    """
    if 1 <= month_num <= 12:
        months = 'JanFebMarAprMayJunJulAugSepOctNovDec'
        pos = (month_num - 1) * 3
        return months[pos:pos + 3]
    else:
        print("Invalid month number, must be 1-12")
        return None

