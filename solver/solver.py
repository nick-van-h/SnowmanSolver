import numpy as np
from datetime import datetime
from checker import traverseEqualFields, fieldIsSolution
from fieldfinder import getnextfields


def moveAndUpdate(field, xys, dir):
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
        return validMove

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


def resolveNextPositions(fields, xys, bigcounter = []):
    bigcounter[0]+=1
    #retrieve list of next possible positions & loop
    #posses = getPossiblePositions(fields[len(fields)-1], xys[len(xys)-1])
    
    posses = getnextfields(fields[len(fields)-1], xys[len(xys)-1])
    for nextpos in posses:
        bp = [4, 2]
        #Teleport to next position
        #Append field and pos
        xys.append(nextpos[0])
        field = fields[len(fields)-1].copy()
        fields.append(field)

        if xys[len(xys)-1] == bp:
            xys = xys
        
        #Perform move action L/U/R/D according direction
        #Append current field and pos
        pos = xys[len(xys)-1].copy()
        xys.append(pos)

        field = fields[len(fields)-1].copy()
        fields.append(field)
        
        #Resolve current field according to direction
        valid = moveAndUpdate(fields[len(fields)-1], xys[len(xys)-1], nextpos[1])
        
        if xys[len(xys)-1] == bp:
            xys = xys
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

        #Remove field and pos from direction move action
        fields.pop()
        xys.pop()

        #Remove field and pos from teleport action
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
