def getIdx(pos):
    return str(pos[0])+","+str(pos[1])

def addIfWalkable(graph, field, x, y, dir):
    if dir == 1:
        nx = x+1
        ny = y
    elif dir == 2:
        nx = x
        ny = y+1
    elif dir == 3:
        nx = x-1
        ny = y
    elif dir == 4:
        nx = x
        ny = y-1

    key = str(x)+","+str(y)
    if key not in graph:
        graph[key] = set()

    val = str(nx)+","+str(ny)
    arr = set()
    if nx >= len(field) or ny >= len(field[x]) or nx < 0 or ny < 0:
        return 0
    if field[nx][ny] == 0 or field[nx][ny] == 1 or field[nx][ny] == -2:

        arr = graph[key]
        arr.add(val)
        graph[key] = arr

def populateGraph(graph, field, start, end):
    for i in range(0, len(field)):
        for j in range(0, len(field[i])):
            if (field[i][j] == 0 or field[i][j] == 1 or field[i][j] == -2):
                addIfWalkable(graph, field, i, j, 1)
                addIfWalkable(graph, field, i, j, 2)
                addIfWalkable(graph, field, i, j, 3)
                addIfWalkable(graph, field, i, j, 4)


def findPathFromGraph(graph, start, end, path=[]):
    startstr = str(start[0])+","+str(start[1])
    endstr = str(end[0])+","+str(end[1])
    path = path + [startstr]
    if startstr == endstr:
        return path
    if startstr not in graph:
        return None
    for node in graph[startstr]:
        if node not in path:
            newpath = findPathFromGraph(graph, node, endstr, path)
            if newpath: return newpath
    return None

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

def findpath(field, start, end): 
    graph = {}
    populateGraph(graph, field, start, end)
    path = shortest_path(graph, getIdx(start), getIdx(end))
    #path = findPathFromGraph(graph,start,end)
    return path

def getDirFromCoords(start, end):
    if start[0] > end[0]:
        return "L"
    if start[0] < end[0]:
        return "R"
    if start[1] > end[1]:
        return "U"
    if start[1] < end[1]:
        return "D"

def getDirectionsFromCoordinates(fields, xys):
    fullcoords = []
    fullcoords.append(xys[0].copy())
    fulldirs = []
    for i in range (1, len(fields)):
        coords = findpath(fields[i], xys[i-1], xys[i])
        if coords is not None:
            for j in coords:
                txt = j.split(",")
                coord = [int(x) for x in txt] 
                fullcoords.append(coord)

                if fullcoords[len(fullcoords)-2] != fullcoords[len(fullcoords)-1]:
                    fulldirs.append(getDirFromCoords(fullcoords[len(fullcoords)-2], fullcoords[len(fullcoords)-1]))
                    #print(fullcoords[len(fullcoords)-2], fulldirs[len(fulldirs)-1], fullcoords[len(fullcoords)-1])
            #print(fields[i])
    #print (fulldirs)
    return fulldirs

        

