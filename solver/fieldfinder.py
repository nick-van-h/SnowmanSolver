def getAsStr(x, y)
    return str(x)+","+str(y)

def getPosFromDir(pos, dir)
    x = pos[0]
    y = pos[1]
    if dir == 1:
        nx = x+1
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
    if key not in graph:
        if field[nx][ny] == 0 or field[nx][ny] == 1:
            posses = []
            for i in range(1,5):
                if addPosToPath(field, pos, path, nextfields, i):
                    posses.append([nx, ny])
            
            graph[getAsStr(x,y)] = posses
            return True
        else:
            if field[nx][ny] > 1 or field[nx][ny] == -2:
                if key not in nextfields:
                    nextfields[getAsStr(x,y)] = []
                arr = nextfields[key]
                arr.append([[x,y],dir])
                graph[key] = arr
                
            return False
    else:
        return True

def getnextfields(field, pos):
    path = {}
    nextfields = {}

    addPosToPath(field, pos, path, nextfields)
    return nextfields