"""
Parse custom inputs from document. 

"""
from typing import Union, Optional
from backend.custom_dataclasses import Definition, OrderedProperty, UnorderedProperty
from pathlib import Path
import re


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


def read_markdown_file(filename: Path) -> list[str]:
    with open(filename, "r") as f:
        return [x for x in f.read().split("\n\n") if x != ""]


def parse_markdown_file(
    filename: Path,
) -> list[Optional[Union[Definition, OrderedProperty, UnorderedProperty]]]:
    """Parse markdown file into a list of objects.
    Args:
        filename : path to markdown file.
    Returns:
        list of objects.
    """
    file: list[str] = read_markdown_file(filename)
    results: list[Optional[Union[Definition, OrderedProperty, UnorderedProperty]]] = []
    for i in range(len(file)):
        line = file[i]
        if "=" in line:
            key, value = split_first_occurance(line, "=")
            results.append(Definition(value1=key, value2=value))
        if ":" in line:
            j = 1
            collection = True
            unordered_set = set()
            ordered_list = []
            while collection:
                if i + j < len(file):
                    next_line = file[i + j]
                    if next_line.startswith("-"):
                        for bullet in next_line.split("\n"):
                            unordered_set.add(bullet.replace("-", ""))

                    elif check_string_starts_numeric(next_line):
                        for bullet in next_line.split("\n"):
                            ordered_list.append(bullet.replace("-", ""))
                    else:
                        j -= 1
                        break
                    j += 1
                else:
                    break
            i += j
            if len(unordered_set) > 0:
                results.append(
                    UnorderedProperty(name=line.replace(":", ""), value=unordered_set)
                )
            elif ordered_list != []:
                results.append(
                    OrderedProperty(name=line.replace(":", ""), value=ordered_list)
                )
    return results
