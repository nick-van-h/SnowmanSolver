import numpy as np
from datetime import datetime
from fieldrunner import startsolve
from layout import getpos, getfield



def run():

    print(datetime.now(), "Start analyzing")
    startsolve(getfield(), getpos())
    print(datetime.now(), "Analysis finished")
