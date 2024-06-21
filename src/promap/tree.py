from typing import Any
import graphviz as gv

from .models import Task


def build_tree(
    tasks: list[Task],
    dep_attrs: dict[str, Any] = {},
    weak_attrs: dict[str, Any] = {'color': '#aaaaaa'},
) -> gv.Digraph:
    g = gv.Digraph('tasks')
    g.attr('node', fontname='Helvetica,Arial,sans-serif')
    g.attr('edge', fontname='Helvetica,Arial,sans-serif')
    g.attr('graph', fontsize='30', labelloc='t', label='', splines='true', overlap='false', rankdir='LR')
    for t in tasks:
        g.node(t.key, t.render(), **t.attrs)
        for d in t.dep:
            g.edge(d, t.key, **dep_attrs)
        for d in t.weak:
            g.edge(d, t.key, **weak_attrs)
    return g
