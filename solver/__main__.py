from datetime import datetime
from fieldrunner import startsolve
from layout import getpos, getfield

if __name__ == '__main__':
    #Kick off solver
    print(datetime.now(), "Start analyzing")
    startsolve(getfield(), getpos())
    print(datetime.now(), "Analysis finished")