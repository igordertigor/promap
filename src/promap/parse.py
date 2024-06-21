from yaml import safe_load

from .models import Task, ConfigSchema


def parse(filename: str) -> list[Task]:
    with open(filename) as f:
        return ConfigSchema(**safe_load(f)).tasks
