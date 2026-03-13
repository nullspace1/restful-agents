from __future__ import annotations

from enum import Enum
from typing import Any, TypedDict, Union


class OperationStatus(Enum):
    CONTINUE = 1
    STOP = 2
    FAIL = 3
    


type primitive = Union[str, int, float, bool]
type op_result = Union[primitive, dict[str, op_result], list[op_result]]


class OperationResult(TypedDict):
    status: OperationStatus
    output: Any
