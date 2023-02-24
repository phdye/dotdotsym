import sys
import re

from typing import Any

import click

# ------------------------------------------------------------------------------

from ..api import dot_dot_sym

# ------------------------------------------------------------------------------


def __getattr__(name: str) -> Any:

    if name.startswith('_dot_'):
        name = '.' + name[5:]

    if name in globals():
        return globals()[name]

    # print(": dotdotsym.tree.__getattr__ ( '%s' )" % ( name ))

    re_symtree_name = re.compile(r"^(\w|.)(\w|.)*$", re.UNICODE)

    if not re.match(re_symtree_name, name):
        raise AttributeError("Invalid symtree name '{}' - does not match '{}'"
                             .format(name, re_symtree_name))

    def create_symtree(args=sys.argv[1:]):
        @click.command()
        @click.argument("tree_name", type=str)
        @click.option(
            "--verbose",
            "-v",
            default=0,
            count=True,
            help="print actions taken, specify more than one to increase detail")
        def main(tree_name, verbose):
            return dot_dot_sym(tree_name=tree_name, verbose=verbose)
        args.append(name)
        exit(main(args))

    return create_symtree

# ------------------------------------------------------------------------------
