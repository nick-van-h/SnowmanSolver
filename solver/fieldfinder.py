#Goal: Returns possible next positions to move to

def getAsStr(x, y):
    return str(x)+","+str(y)

def getPosFromDir(pos, dir):
    x = pos[0]
    y = pos[1]
    if dir == 1:
        nx = x-1
        ny = y    
    elif dir == 2:
        nx = x
        ny = y-1
    elif dir == 3:
        nx = x+1
        ny = y
    elif dir == 4:
        nx = x
        ny = y+1
    else:
        nx = x
        ny = y
    
    return [nx, ny]


def addPosToPath(field, pos, path, nextfields, dir = 0):
    x = pos[0]
    y = pos[1]
    nextpos = getPosFromDir(pos, dir)
    nx = nextpos[0]
    ny = nextpos[1]

    key = getAsStr(nx,ny)
    #Check if new pos is already in graph and if new pos is walkable

    if field[nx][ny] == 0 or field[nx][ny] == 1:
        if key not in path:
            path[key] = 1
            for i in range(1,5):
                addPosToPath(field, nextpos, path, nextfields, i)
    else:
        if field[nx][ny] > 1 or field[nx][ny] == -2:
            if key not in nextfields:
                nextfields[key] = []
            arr = nextfields[key]
            arr.append([[x,y],dir])
            nextfields[key] = arr

def getnextfields(field, pos):
    path = {}
    nextfields = {}
    nextfieldsarr = []

    addPosToPath(field, pos, path, nextfields)
    for key in nextfields:
        arr = nextfields[key]
        for i in range(0,len(arr)):
            nextfieldsarr.append(arr[i])

    return nextfieldsarr