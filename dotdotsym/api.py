#!/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------

"""
    Maintain parallel tree rooted at .../<name>' with symlinks at each level '<d>'
    a symlink './<name>' to ../<name>/\$(basename <d>.

    Example:  A project named 'example' with a log tree parallel to its src tree.

       ~user/project/example/
           ../log
             ../src
               ../command
               ../lib
           ../src/log 		--> ../log/src
             ../command/log	--> ../log/command
             ../lib/log		--> ../log/log
"""

# ------------------------------------------------------------------------------

import os
import sys

from pathlib import Path

import click

from .chdir import ChDir

# ------------------------------------------------------------------------------

__all__ = ['dot_dot_sym', 'main']

_default_tree_name = 'symtree'

# ------------------------------------------------------------------------------


def dot_dot_sym(tree_name, dotted=False, verbose=0):
    # On POSIX, directory entires starting with a '.' are not shown in 'ls'
    # listings unless requested for with '-a'.
    if dotted :
        tree_name = f".{treename}"
    _worker(tree_name, os.getcwd(), None, verbose)

# ------------------------------------------------------------------------------

# Search upward for writable /.../<tree-name>

def _worker(tree_name, dir, name, verbose=0):

    if verbose >= 3:
        print (
            "dot_dot_sym_worker():  tree_name = '{}', dir = '{}', name = '{}'" .format(
                tree_name,
                dir,
                name))

    # If '<dir>/<tree_name>/.' exists and is fully accessible, return
    symDir = Path ( os.path.join(dir, tree_name) )
    if symDir.exists():
        if not os.access(symDir / '.', os.R_OK|os.W_OK|os.X_OK):
            issues = Path()
            if not os.access(str(symDir / '.'), os.R_OK):
                issues /= 'read'
            if not os.access(symDir / '.', os.W_OK):
                issues /= 'write'
            if not os.access(symDir / '.', os.X_OK):
                issues /= 'list'
            raise Exception(
                f"Directory '{symDir}' exists but you may not {str(issues)}")
        return True
    # elif os.path.islink ( symDir ) :
    #     raise Exception ( "Link '{}' exists but it's target does not.".format ( symDir ) )

    # Otherwise, recurse to ensure that '../<tree-name>' exists and is writable
    parent, name = os.path.split(dir)
    if (len(name) <= 0):
        raise Exception(
            "Walked upward to root '{}', no '{}' directory found.".format(
                parent, tree_name))

    _worker(tree_name, parent, name, verbose)

    if verbose >= 2:
        print ("Writable directory '{}'.".format(symDir))

    # Then, create destination directory and relative symbolic link

    # Must chdir(), as Windows evaluates relative symbolic links from CWD.
    with ChDir(dir):
        rdst = os.path.join('..', tree_name, name)
        if not os.path.exists(rdst):
            if verbose >= 1:
                print ("- creating '{}'".format(rdst))
            try:
                os.mkdir(rdst)
            except OSError as e:
                raise OSError("In '{}', unable to create directory '{}' : {}"
                              .format(dir, rdst, str(e)))

        # When ready, support Windows links using win32api.w32symlink()
        if verbose >= 1:
            print (
                "- linking '{}' --> '{}' ".format(os.path.join(dir, tree_name), rdst))
        try:
            if os.path.islink(tree_name):
                os.unlink(tree_name)
            os.symlink(rdst, tree_name)
        except OSError as e:
            raise OSError("In '{}', unable to create symlink '{}' to '{}' : {}"
                          .format(dir, tree_name, rdst, str(e)))

# ------------------------------------------------------------------------------


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

# ------------------------------------------------------------------------------


if __name__ == '__main__':
    exit(main(sys.argv[1:]))

# ------------------------------------------------------------------------------
