#!/bin/python
# -*- coding: utf-8 -*-


"""dotdotsym.log : script to execute dot_dot_sym() to maintain a 'build' parallel tree."""


from dotdotsym import dot_dot_sym


def main():
    return (dot_dot_sym(tree_name='log'))


if __name__ == '__main__':
    exit(main())
