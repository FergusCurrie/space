from dataclasses import dataclass


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
