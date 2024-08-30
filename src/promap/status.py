from enum import Enum

class Status(str, Enum):
    focus = 'focus'
    current_milestone = 'current_milestone'
    milestone = 'milestone'
    started = 'started'
    testing = 'testing'
    default = 'default'
    done = 'done'
    postponed = 'postponed'
    wontdo = 'wontdo'

