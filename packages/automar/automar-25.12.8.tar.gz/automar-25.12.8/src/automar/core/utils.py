# -*- coding: utf-8 -*-
"""Module containing utility functions"""


def getmaybe(xx, yy, zz):
    ww = xx.get(yy)
    if ww is None:
        return zz
    return ww
