#TODO: Make class

        
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

def findpath(field, start, end): 
    graph = {}
    populateGraph(graph, field, start, end)
    return findPathFromGraph(graph,start,end)

    """
    #TODO: Make class
    g = graph()
    g.populateGraph(graph, field, start, end)
    return g.findPathFromGraph(graph,start,end)
    """