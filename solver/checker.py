
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