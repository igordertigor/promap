import typer

from .parse import parse
from .tree import build_tree
from .models import Status
from .filter_by_status import filter_by_status


app = typer.Typer(name='promap')


@app.command()
def asdot(filename: str, outfile: str, exclude: list[str] = [Status.done]):
    nodes = parse(filename)
    nodes = filter_by_status(nodes, exclude=set(exclude))
    t = build_tree(nodes)
    with open(outfile, 'wb') as f:
        f.write(t.pipe(format='pdf'))


if __name__ == '__main__':
    app()
