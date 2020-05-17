
"""
def fieldIsUnique(fields, xys, posses, allfields, allposses):
    x = xys[len(xys)-1][0]
    y = xys[len(xys)-1][1]
    field = fields[len(fields)-1]
    nextposses = []
    for i in posses:
        nextposses.append(i[0])

    if field[x][y] == -2:
        return True
    for i in range(len(fields)-1):
        #if (fields[i] == fields[len(fields)-1]).all() and xys[i] == xys[len(xys)-1]:
        if (fields[i] == fields[len(fields)-1]).all() and xys[i] in nextposses:
            #print("Recursive move, equal to previous step = ", i)
            return False
    
    for i in range(len(allfields)-1):
        if (fields[len(fields)-1] == allfields[i]).all and xys[len(xys)-1] in allposses[i]:
            return False
    
    return True
"""

def fieldIsUnique(field = [], posses = [], allfields = [], allposses = []):
    
    for i in range(len(allfields)-1):
        if (field == allfields[i]).all():
            if (posses == allposses[i]):
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

def fieldIsSolvable(field):
    #Iterate over field, count items & preliminary check if solvable
    counter = [0, 0, 0, 0] #[Patches, lvl1 balls, lvl2 balls, lvl3 balls]
    for x in range(len(field)):
        for y in range(len(field[x])):
            #Count
            if field[x][y] > 0:
                if field[x][y] < 10:
                    #Single item
                    counter[field[x][y] - 1] += 1
                elif field[x][y] < 100:
                    #Stack of 2 balls
                    counter[(field[x][y]%10) - 1] += 1
                    counter[(field[x][y]//10) - 1] += 1
                else:
                    #Stack of 3
                    counter[1] += 1
                    counter[2] += 1
                    counter[3] += 1

            #Check for incomplete ball(s) in corner
            if field[x][y] > 1 and field[x][y] != 4 and field[x][y] != 43 and field[x][y] != 432:
                numwalls = 0
                if field[x+1][y] == -1:
                    numwalls += 1
                if field[x][y+1] == -1:
                    numwalls += 1
                if field[x-1][y] == -1:
                    numwalls += 1
                if field[x][y-1] == -1:
                    numwalls += 1
                if numwalls > 1:
                    return False

    #Check if number of balls present make enough to complete all snowmans
    numsnowmans = (counter[1]+counter[2]+counter[3]) / 3
    if counter[1] < numsnowmans or counter[2] > (2*numsnowmans) or counter[3] > numsnowmans:
        #Not enough small balls or more than needed medium balls or more than needed big balls
        return False
    
    return True
