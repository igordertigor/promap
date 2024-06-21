from pydantic import BaseModel, Field

from .color import Color
from .status import Status


class Style(BaseModel):
    col: Color = '#'
    fg: Color
    bg: Color


class Task(BaseModel):
    key: str
    desc: str
    status: Status = Status.default
    dep: list[str] = Field(default_factory=list)
    weak: list[str] = Field(default_factory=list)
    style: Style = Style()
