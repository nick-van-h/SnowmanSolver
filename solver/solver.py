import numpy as np
from datetime import datetime
from fieldrunner import startsolve



def run():
    #Main entry code
    pos = [2, 5]
    xy = []
    xy.append(pos)

    field = [
    # [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11] 
    [-1,-1,-2,-1,-1,-1,-2,-1,-1,-1,-1,-1], #0
    [-1, 0, 0, 0,-1, 0, 0, 0,-1, 1, 1,-1], #1
    [-1, 0, 0, 0,-1, 2, 1, 0,-1, 1, 1,-1], #2
    [-1, 0, 0, 0, 0, 2, 1, 0,-1, 1, 1,-1], #3
    [-1, 0, 0, 0,-1, 2, 1, 0,-1, 1, 1,-1], #4
    [-1, 0, 0, 0,-1, 0, 0, 0,-1, 1, 1,-1], #5
    [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0,-1], #6
    ]
    field = np.transpose(field)
    fields = []
    fields.append(field)

    print(datetime.now(), "Start analyzing")
    startsolve(fields, xy)
    #resolveNextField(fields, xy)
    print(datetime.now(), "Analysis finished")


    """
    field = [
    # [ 0, 1, 2, 3, 4, 5, 6, 7, 8] 
    [-1,-1,-2,-1,-1,-1,-1,-1,-1], #0
    [-1, 1, 1, 1, 2, 1, 1, 1,-1], #1
    [-1, 1, 1, 2, 1, 2, 1, 1,-1], #2
    [-1, 1, 1,-1,-1,-1, 1, 1,-1], #3
    [-1, 1, 1, 2, 1, 2, 1, 1,-1], #4
    [-1, 1, 1, 1, 2, 1, 1, 1,-1], #5
    [-1,-1,-1,-1,-1, 0,-1, 0,-1], #6
    [-1,-1,-1,-1,-1, 0, 0, 0,-1], #7
    [-1,-1,-1,-1,-1,-1,-1,-1,-1], #8
    ]
    """