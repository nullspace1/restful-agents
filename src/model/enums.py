from __future__ import annotations

from enum import Enum


class OperationType(Enum):
    POST = "post"
    PATCH = "patch"
    DELETE = "delete"
    GET = "get"


class Status(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
