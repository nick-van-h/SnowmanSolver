import numpy as np
from datetime import datetime
from pathfinder import findpath

#TODO: Make class for graph




def addPosIfReachable(posses, field, x, y, nx, ny):
    if field[nx][ny] == 0 or field[nx][ny] == 1:
        start = str(x)+","+str(y)
        end = str(nx)+","+str(ny)
        if findpath(field, start, end) is not None:
            nextpos = []
            nextpos.append(nx)
            nextpos.append(ny)
            posses.append(nextpos)

def getPossiblePositions(field, xy):
    x = xy[0]
    y = xy[1]
    posses = []
    #Loop through field
    #Check if field is ball
    #Check if adjacent fields are reachable & add to array
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > 1 or field[i][j] == -2:
                #addPosIfReachable(posses, field, x, y, i, j)
                addPosIfReachable(posses, field, x, y, i, j + 1)
                addPosIfReachable(posses, field, x, y, i, j - 1)
                addPosIfReachable(posses, field, x, y, i + 1, j)
                addPosIfReachable(posses, field, x, y, i - 1, j)
    return posses

def moveAndSolve(field, xys, dir):
    validMove = True
    x = xys[0]
    y = xys[1]
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
    elif nf == -2:
        nnf = -20
    else:
        nnf = -10

    #Solve action dependent on next field
    if nf == -2:
        #Move into gate
        x = nx
        y = ny
    elif nf == -1:
        #Walk into wall
        validMove = False
        reason = "Move into object"
        return validMove
    elif nf == 0 or nf == 1:
        #Regular walk, no use
        x = nx
        y = ny
        return False
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
            validMove = False #no use
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
        
    xys[0] = x
    xys[1] = y
    
    #if not validMove:
        #print(reason)

    return validMove

def traverseEqualFields(fields, xys, posses):
    x = xys[len(xys)-1][0]
    y = xys[len(xys)-1][1]
    field = fields[len(fields)-1]
    if field[x][y] == -2:
        return True
    for i in range(len(fields)-1):
        #if (fields[i] == fields[len(fields)-1]).all() and xys[i] == xys[len(xys)-1]:
        if (fields[i] == fields[len(fields)-1]).all() and xys[i] in posses:
            #print("Recursive move, equal to previous step = ", i)
            return False
    
    return True

def fieldIsSolution(field, xys):
    x = xys[0]
    y = xys[1]
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


        
"""
def resolveNextPos(fields, xys, dir = 0, lvl = 0, dirs = [0]):
    posses = []
    getPossiblePositions(fields[len(fields)-1], xys[len(xys)-1], posses)
    for nextpos in posses:
        #TODO: Fix correct appending of fields & posses
        xys.append(nextpos)
        field = fields[len(fields)-1].copy()
        fields.append(field)

        for i in range(4, 0, -1):
            resolveNextField(fields, xys, i, lvl+1, dirs)
        
        fields.pop()
        xys.pop()

def resolveNextField(fields, xys, dir = 0, lvl = 0, dirs = [0]):

    #duplicate append last entry of field, append last dir
    field = fields[len(fields)-1].copy()
    pos = xys[len(xys)-1].copy()

    #Resolve field
    if dir > 0:
        fields.append(field)
        dirs.append(dir)
        xys.append(pos)
        valid = moveAndSolve(fields[len(fields)-1], xys[len(xys)-1], dir)
        valid = valid and traverseEqualFields(fields, xys)
    else:
        valid = True

    #check for solution
    if fieldIsSolution(fields[len(fields)-1], xys[len(xys)-1]):
        newdirs = ["L" if x == 1 else x for x in dirs]
        newdirs = ["U" if x == 2 else x for x in newdirs]
        newdirs = ["R" if x == 3 else x for x in newdirs]
        newdirs = ["D" if x == 4 else x for x in newdirs]
        print(datetime.now(), "Solution: ", newdirs)
    elif valid and lvl < 70:
        #for i in range(4, 0, -1):
            #resolveNextField(fields, xys, i, lvl+1, dirs)
            #TODO: Fix ping-pong recursion
            resolveNextPos(fields, xys, 0, lvl+1, dirs)

    fields.pop()
    dirs.pop()
    xys.pop()
"""

def resolveNextPositions(fields, xys, bigcounter = []):
    bigcounter[0]+=1
    #retrieve list of next possible positions & loop
    posses = getPossiblePositions(fields[len(fields)-1], xys[len(xys)-1])
    for nextpos in posses:
        if nextpos != xys[len(xys)-1] or len(fields) == 1: #Skip same position unless first action
            #Append field and pos
            xys.append(nextpos)
            field = fields[len(fields)-1].copy()
            fields.append(field)
            
            #Perform move action L/U/R/D
            for dir in range (1,5):
                #Append current field and pos
                pos = xys[len(xys)-1].copy()
                xys.append(pos)

                field = fields[len(fields)-1].copy()
                fields.append(field)
                
                #Resolve current field according to direction
                valid = moveAndSolve(fields[len(fields)-1], xys[len(xys)-1], dir)
                valid = valid and traverseEqualFields(fields, xys, posses)
                
                #Check if move is solution or valid
                if valid and len(fields) < 50:
                    if fieldIsSolution(fields[len(fields)-1], xys[len(xys)-1]):
                        """
                        newdirs = ["L" if x == 1 else x for x in dirs]
                        newdirs = ["U" if x == 2 else x for x in newdirs]
                        newdirs = ["R" if x == 3 else x for x in newdirs]
                        newdirs = ["D" if x == 4 else x for x in newdirs]
                        """
                        print(datetime.now(), "Solution: ", xys)
                    else:
                        #Iterate next field
                        resolveNextPositions(fields,xys,bigcounter)

                fields.pop()
                xys.pop()

            #Remove field and pos
            fields.pop()
            xys.pop()
        


def startsolve(field, pos):
    #Make positions array
    xys = []
    xys.append(pos)
    
    #Make fields array
    field = np.transpose(field.copy())
    fields = []
    fields.append(field)

    #Kick off recursive function
    #resolveNextField(fields, xys)

    count = []
    count.append(0)
    resolveNextPositions(fields,xys,count)
