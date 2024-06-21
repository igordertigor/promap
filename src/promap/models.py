from typing import Self
import textwrap
from pydantic import BaseModel, Field, model_validator

from .color import Color, get_color
from .status import Status


class Task(BaseModel):
    key: str
    desc: str
    status: Status = Status.default
    dep: list[str] = Field(default_factory=list)
    weak: list[str] = Field(default_factory=list)

    def render(self) -> str:
        text = '<br />'.join(
            textwrap.wrap(
                self.desc.replace('"', "'").replace('&', '+'), width=40
            )
        )
        return ''.join(
            [
                '<<table border = "0">',
                f'<th><td bgcolor="#dddddd">{self.key}</td></th>',
                f'<tr><td>{text}</td></tr>',
                '</table>>',
            ]
        )

    @property
    def attrs(self) -> dict[str, str]:
        out = {
            'shape': 'box',
            'style': 'filled',
            'fillcolor': get_color(self.status),
        }
        return out


class ConfigSchema(BaseModel):
    categories: dict[str, str]
    tasks: list[Task]

    @model_validator(mode='after')
    def ensure_valid_task_keys(self) -> Self:
        for task in self.tasks:
            cat = task.key.split('.')[0]
            if cat not in self.categories:
                raise ValueError(
                    f'Task with key {task.key} does not fit with categories {set(self.categories)}'
                )
        return self
