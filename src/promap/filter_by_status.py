from .models import Task, Status
def filter_by_status(tasks: list[Task], exclude: set[Status]) -> list[Task]:
    result = [t for t in tasks if t.status not in exclude]
    reject = [t.key for t in tasks if t.status in exclude]
    for t in result:
        t.dep = [d for d in t.dep if d not in reject]
        t.weak = [d for d in t.weak if d not in reject]
    return result
