import numpy as np
from datetime import datetime
from fieldrunner import startsolve
from layout import getpos, getfield

from fieldfinder import getnextfields


def run():

    print(datetime.now(), "Start analyzing")
    getnextfields()
    startsolve(getfield(), getpos())
    print(datetime.now(), "Analysis finished")
