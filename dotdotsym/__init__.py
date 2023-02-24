# ------------------------------------------------------------------------------

version = '1.4.0'

# ------------------------------------------------------------------------------

# from .api import *

# The single line above, is replaced by all of the following to support dynamic
# loading of 'api.py'.

# All to allow version to be loaded from __init__.py rather than version.py

# The value lies not in the destination but in the treasured knownlege one
# acquires by plotting the route and surmounting the obstacles along the way.

# ------------------------------------------------------------------------------

# from typing import Any

# ------------------------------------------------------------------------------


def __getattr__(name):
     # type: (str) -> Any
    if name in globals():
        return globals()[name]
    # print(": dotdotsym.__getattr__ ( '%s' )" % ( name ))
    if name in ['dot_dot_sym', 'main']:
        return import_star(name, 'api')
    raise AttributeError("No such attribute '{}'".format(name))

# ------------------------------------------------------------------------------


def import_star(name, module):

    # FIXME:  use __path__

    from importlib import import_module
    import sys

    m = import_module('.' + module, __name__)

    m_dict = vars(m)

    for attr, key in m_dict.items():
        globals()[attr] = m_dict[attr]

    if name in globals():
        return globals()[name]

    raise AttributeError(
        "Internal error in package '%s', '.%s' does not define '%s'" %
        (__name__, module, name))

# ------------------------------------------------------------------------------
