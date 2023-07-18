"""
Parse custom inputs from document. 

"""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class UnorderedProperty:
    name: str
    value: set[str]


@dataclass
class OrderedProperty:
    name: str
    value: list[str]


@dataclass
class Definition:
    value1: str
    value2: str


def check_string_starts_numeric(my_string: str) -> bool:
    if re.match(r"^\d", my_string):
        return True
    return False


def split_first_occurance(my_string, pattern) -> list[str]:
    """Split string on first occruance of pattern.

    Args:
        my_string (str): string to split
        pattern (str): string to split on

    Returns:
        list[str]: list of length 2 with first element before pattern and second element after pattern
    """
    split = my_string.split(pattern)
    i = my_string.index(pattern)
    result = [split[0], my_string[i + 1 :].strip()]
    return result


def read_markdown_file(filename: str):
    with open(filename, "r") as f:
        return [x for x in f.read().split("\n\n") if x != ""]


def parse_markdown_file(
    filename: Path,
) -> list[UnorderedProperty, OrderedProperty, Definition]:
    file: str = read_markdown_file(filename)
    """Parse markdown file into a list of objects. 
    
    Args:
        filename : path to markdown file.
    Returns:
        list of objects.
    """
    results = []
    for i in range(len(file)):
        line = file[i]
        if "=" in line:
            key, value = split_first_occurance(line, "=")
            results.append(Definition(value1=key, value2=value))
        if ":" in line:
            j = 1
            collection = True
            unordered_list = set()
            ordered_list = []
            while collection:
                if i + j < len(file):
                    next_line = file[i + j]
                    if next_line.startswith("-"):
                        unordered_list.add(next_line.replace("-", ""))
                    elif check_string_starts_numeric(next_line):
                        ordered_list.append(next_line.replace("-", ""))
                    else:
                        j -= 1
                        break
                    j += 1
                else:
                    break
            i += j
            if unordered_list != []:
                results.append(
                    UnorderedProperty(name=line.replace(":", ""), value=unordered_list)
                )
            elif ordered_list != []:
                results.append(
                    OrderedProperty(name=line.replace(":", ""), value=ordered_list)
                )
    results
