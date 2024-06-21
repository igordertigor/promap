from typing import Annotated
from pydantic import AfterValidator
from .status import Status


def is_color(s: str) -> str:
    if len(s) != 7:
        raise ValueError()
    if s[0] != '#':
        raise ValueError()
    int(s[1:], 16)  # check that we can interprete the tail as a hex number
    return s


Color = Annotated[str, AfterValidator(is_color)]


def get_color(s: Status) -> Color:
    colors = {
        Status.default: '#ffeebb',
        Status.focus: '#ffffee',
        Status.postponed: '#eeeeee',
        Status.current_milestone: '#ffaaaa',
        Status.started: '#aaffcc',
    }
    return colors.get(s, colors[Status.default])
