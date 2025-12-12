from dataclasses import dataclass
from datetime import timedelta
from typing import Literal
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

@dataclass
class TaskStatus:
    status: Literal["done", "notrunning", "success", "failure", "terminated"]
    task_id: str
    lookback: timedelta | None = None

@dataclass
class ExitCode:
    value: int | str
    operator: Literal["=", "!=", ">", "<", ">=", "<="]
    task_id: str
    lookback: timedelta | None = None

@dataclass
class Variable:
    name: str
    operator: Literal["=", "!=", ">", "<", ">=", "<="]
    value: int | str

@dataclass
class Condition:
    condition: Literal["and", "or"]
    children: list[TaskStatus | Self]
