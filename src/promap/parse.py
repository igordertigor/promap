from yaml import safe_load

from .models import ConfigSchema


def parse(filename: str) -> ConfigSchema:
    with open(filename) as f:
        return ConfigSchema(**safe_load(f))
