import numpy as np
from datetime import datetime

#TODO: Make class for graph

def addIfWalkable(graph, field, x, y, nx, ny):
    key = str(x)+","+str(y)
    val = str(nx)+","+str(ny)
    arr = []
    if nx >= len(field) or ny >= len(field[x]) or nx < 0 or ny < 0:
        return 0
    if field[nx][ny] == 0 or field[nx][ny] == 1 or field[nx][ny] == -2:
        if key not in graph:
            graph[key] = []
        arr = graph[key]
        arr.append(val)
        graph[key] = arr

def populateGraph(graph, field, start, end):
    for i in range(0, len(field)):
        for j in range(0, len(field[i])):
            if (field[i][j] == 0 or field[i][j] == 1):
                addIfWalkable(graph, field, i, j, i, j + 1)
                addIfWalkable(graph, field, i, j, i, j - 1)
                addIfWalkable(graph, field, i, j, i + 1, j)
                addIfWalkable(graph, field, i, j, i - 1, j)


def findPathFromGraph(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    for node in graph[start]:
        if node not in path:
            newpath = findPathFromGraph(graph, node, end, path)
            if newpath: return newpath
    return None

def findPath(field, start, end): 

    graph = {}
    populateGraph(graph, field, start, end)
    return findPathFromGraph(graph,start,end)

def resolveNextPos(fields, xy, dir = 0, lvl = 0, dirs = [0]):
    posses = []
    getPossiblePositions(fields[len(fields)-1], xy[len(xy)-1], posses)
    for nextpos in posses:
        #TODO: Fix correct appending of fields & posses
        xy.append(nextpos)
        field = fields[len(fields)-1].copy()
        fields.append(field)

        for i in range(4, 0, -1):
            resolveNextField(fields, xy, i, lvl+1, dirs)
        
        fields.pop()
        xy.pop()

def resolveNextField(fields, xy, dir = 0, lvl = 0, dirs = [0]):

    #duplicate append last entry of field, append last dir
    field = fields[len(fields)-1].copy()
    pos = xy[len(xy)-1].copy()

    #Resolve field
    if dir > 0:
        fields.append(field)
        dirs.append(dir)
        xy.append(pos)
        valid = moveAndSolve(fields[len(fields)-1], xy[len(xy)-1], dir)
        valid = valid and traverseEqualFields(fields, xy)
    else:
        valid = True

    """
    #Print layout etc for debugging
    newdirs = ["L" if x == 1 else x for x in dirs]
    newdirs = ["U" if x == 2 else x for x in newdirs]
    newdirs = ["R" if x == 3 else x for x in newdirs]
    newdirs = ["D" if x == 4 else x for x in newdirs]

    print(lvl, newdirs, valid)
    myfield = np.transpose(fields[len(fields)-1].copy())
    myfield[pos[0]][pos[1]] = 5
    for i in range (0, len(myfield)):
        print(myfield[i])
    """
    #check for solution
    if fieldIsSolution(fields[len(fields)-1], xy[len(xy)-1]):
        newdirs = ["L" if x == 1 else x for x in dirs]
        newdirs = ["U" if x == 2 else x for x in newdirs]
        newdirs = ["R" if x == 3 else x for x in newdirs]
        newdirs = ["D" if x == 4 else x for x in newdirs]
        print(datetime.now(), "Solution: ", newdirs)
    elif valid and lvl < 70:
        #for i in range(4, 0, -1):
            #resolveNextField(fields, xy, i, lvl+1, dirs)
            #TODO: Fix ping-pong recursion
            resolveNextPos(fields, xy, 0, lvl+1, dirs)
    


    fields.pop()
    dirs.pop()
    xy.pop()

def addPosIfReachable(posses, field, x, y, nx, ny):
    if field[nx][ny] == 0 or field[nx][ny] == 1:
        start = str(x)+","+str(y)
        end = str(nx)+","+str(ny)
        if findPath(field, start, end) is not None:
            nextpos = []
            nextpos.append(nx)
            nextpos.append(ny)
            posses.append(nextpos)

def getPossiblePositions(field, pos, posses):
    x = pos[0]
    y = pos[1]
    #Loop through field
    #Check if field is ball
    #Check if adjacent fields are reachable & add to array
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > 1 or field[i][j] == -2:
                addPosIfReachable(posses, field, x, y, i, j)
                addPosIfReachable(posses, field, x, y, i, j + 1)
                addPosIfReachable(posses, field, x, y, i, j - 1)
                addPosIfReachable(posses, field, x, y, i + 1, j)
                addPosIfReachable(posses, field, x, y, i - 1, j)

def moveAndSolve(field, xy, dir):
    validMove = True
    x = xy[0]
    y = xy[1]
    #Get next fields coordinates
    if dir == 1:
        nx = x-1
        ny = y
        nnx = x-2
        nny = y
    elif dir == 2:
        nx = x
        ny = y-1
        nnx = x
        nny = y-2
    elif dir == 3:
        nx = x+1
        ny = y
        nnx = x+2
        nny = y
    elif dir == 4:
        nx = x
        ny = y+1
        nnx = x
        nny = y+2
    else:
        validMove = False
        reason = "Invalid direction"

    #Get next fields values
    nf = field[nx][ny]
    if nf >= 0:
        nnf = field[nnx][nny]
    else:
        nnf = -10

    #Solve action dependent on next field
    if nf == -2:
        #Move into gate
        x = nx
        y = ny
    if nf == -1:
        #Walk into wall
        validMove = False
        reason = "Move into object"
    elif nf == 0 or nf == 1:
        #Regular walk
        x = nx
        y = ny
    elif nf == 2 or nf == 3 or nf == 4:
        #Walk into single snowball
        if nnf == -1 or nnf == -2:
            #Roll into object
            validMove = False
            reason = "Roll ball into object"
        elif nnf == 0 or nnf == 1:
            #Move on empty patch (w/wo snow)
            nnf = min(nnf + nf, 4) #Max ball size is 4
            nf = 0
            x = nx
            y = ny
        elif nnf <= nf:
            #Roll into same size or smaller ball
            validMove = False
            reason = "Roll ball into object"
        elif nnf > nf and nnf < 10:
            #Roll into bigger ball
            nnf = (nnf*10) + nf
            nf = 0
            x = nx
            y = ny
        elif nnf > 10:
            #move on other stack
            if nf == 2 and nnf == 43:
                nnf = (nnf*10) + nf
                nf = 0
                x = nx
                y = ny
            else:
                validMove = False
                reason = "Roll ball on invalid stack"
        else:
            #Move on empty patch (w/wo snow)
            nnf = nnf + nf
            nf = 0
            x = nx
            y = ny
    else:
        #Move into stack
        if nnf == 0 or nnf == 1:
            #Roll top ball off
            nnf = nnf + (nf%10)
            nf = nf // 10
        else:
            #Move into object or other ball(s)
            validMove = False
            reason = "Roll stack into object or other ball(s)"

    #Update field field with new calculated values
    if nnf > -10:
        field[nx][ny] = nf
        field[nnx][nny] = nnf
        
    xy[0] = x
    xy[1] = y
    
    #if not validMove:
        #print(reason)

    return validMove

def traverseEqualFields(fields, xy):
    for i in range(len(fields)-1):
        if (fields[i] == fields[len(fields)-1]).all() and xy[i] == xy[len(xy)-1]:
            #print("Recursive move, equal to previous step = ", i)
            return False
    
    return True

def fieldIsSolution(field, xy):
    x = xy[0]
    y = xy[1]
    #Iterate over array and check for completeness
    allBallsGone = True
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > 1 and field[i][j] != 432:
                allBallsGone = False
    
    if field[x][y] == -2 and allBallsGone:
        return True
    else:
        return False

def addT(t):
    t[len(t)-1]=10

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

for i in range(0, len(field)):
    print("x = ", i, field[i])

print(datetime.now(), "Start analyzing")
resolveNextPos(fields, xy)
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