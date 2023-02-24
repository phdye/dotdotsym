from setuptools import setup, find_packages

from dotdotsym import version

setup(
    name='dotdotsym',
    version='1.4',
    description=r"Maintain parallel tree rooted at /.../<name>' with symlinks at each level '<d>' a symlink './<name>' to ../<name>/\$(basename <d>)",
    author='Philip H. Dye',
    author_email='philip@phd-solutions.com',
    # packages=['dotdotsym','dotdotsym.tree'],
    packages=find_packages(),
    requires=['click'],
    # install_requires=[],
    entry_points='''
        [console_scripts]
            dot-dot-sym         = dotdotsym:main
            dot-dot-log         = dotdotsym.tree:log
            ..log               = dotdotsym.tree:log
            dot-dot-snapshot    = dotdotsym.tree:snapshot
            ..snapshot          = dotdotsym.tree:snapshot
            ..snap              = dotdotsym.tree:snapshot
            dot-dot-git         = dotdotsym.tree:_dot_git
            ..git               = dotdotsym.tree:_dot_git
            dot-dot-reference   = dotdotsym.tree:_dot_reference
            ..reference         = dotdotsym.tree:_dot_reference
            ..ref               = dotdotsym.tree:_dot_reference
	'''
)
