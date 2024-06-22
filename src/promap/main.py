import typer
import os
import io
from yaml import safe_dump, safe_load

from .parse import parse
from .tree import build_tree
from .models import Status
from .filter_by_status import filter_by_status


app = typer.Typer(name='promap')


@app.command()
def asdot(filename: str, outfile: str, exclude: list[str] = [Status.done]):
    nodes = parse(filename).tasks
    nodes = filter_by_status(nodes, exclude=set(exclude))
    t = build_tree(nodes)
    with open(outfile, 'wb') as f:
        f.write(t.pipe(format='pdf'))


@app.command()
def clean(filename: str, donefile: str = '', exclude: list[str] = [Status.done], dryrun: bool = False):
    config = parse(filename)
    keep, drop = [], []
    for task in config.tasks:
        if task.status in exclude:
            drop.append(task)
        else:
            keep.append(task)
    dropped_keys = [t.key for t in drop]
    for task in keep:
        task.dep =  [d for d in task.dep if d not in dropped_keys]
        task.weak = [d for d in task.weak if d not in dropped_keys]
    config.tasks = keep

    tasks_out = io.StringIO()
    done_out = io.StringIO()
    safe_dump(config.model_dump(mode='json'), tasks_out)

    if donefile and os.path.exists(donefile):
        with open(donefile) as f:
            done = safe_load(f)
    else:
        done = []

    done += [t.model_dump(mode='json') for t in drop]
    safe_dump(done, done_out)

    print(f'New {filename}')
    print(tasks_out.getvalue())
    print('\n\n')
    print('New done')
    print(done_out.getvalue())

    if dryrun:
        return

    with open(filename, 'w') as f:
        f.write(tasks_out.getvalue())

    if donefile:
        with open(donefile, 'w') as f:
            f.write(done_out.getvalue())

if __name__ == '__main__':
    app()
