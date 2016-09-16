import sys
import os
import math


__author__ = 'User_Admin'

class GridNode:
    def __init__(self,coord,discovered,parent,parentNode,g,h,f):
        self.coord = coord
        self.isDiscovered = discovered
        self.parentCoord = parent
        self.parentNode = parentNode
        self.g = g
        self.h = h
        self.f = f








def main():


    file = open("//Users//Robert//Documents//inputs//8.txt",'r')
    row =  file.readline() # store given row index
    col =  file.readline() # store given column index

    #store read file as matrix
    grid = [[" " for x in range(int(col))] for x in range(int(row))] # null 2d matrix
    initGridSpace(file,grid,row,col)
    file.close()
    #find the start coordinate
    startCoordinate = findStart(grid,row,col)
    goal = findGoal(grid,row,col)
    nodeListIndex = 0
    #declare the open list
    openList = [] #null open list
    #declare the closed list
    closedList = []
    #declare universal visited list
    visited = [] #null visted list

    walkable = [] #null walkable list
    nodeList = [] # List will contain all nodes visted as well as parent node
    costList = []
    heurisitics = []

    #mark start coordiante as visited
    nodeToAppend = newNode(startCoordinate)
    #move start coordiante to lcosed list
    nodeToAppend.parentCoord = None
    nodeToAppend.parentNode = None
    nodeToAppend.g = 0
    nodeToAppend.h = 0
    nodeToAppend.f = 0

    #evaluate closed list node :: -> closed list = eval node
    openList.append(nodeToAppend) #visited
    closedList.append(nodeToAppend)
    visited.append(nodeToAppend.coord)
    # ____________________   start loop
    #while len(visited) != (int(row) * int(col)):
    r = int(row)
    c = int(col)
    while len(visited) <= r*c:

        #find walkable nodes [element 1, element 2, element 3,... etc]  closedList[i++]
        walkable = []
        walkableadj = searchForWalkable(closedList[nodeListIndex].coord,int(row),int(col),grid)
        walkable.extend(walkableadj)
        #walkable = [] -> walkable = findWalkable
        open_list = returnArrayByCoord(openList)

        tempList = set(walkable) & set(visited) #remove duplicates
        nodesToRemove = list(tempList)


        if nodesToRemove:
            for items in nodesToRemove:
                walkable.remove(items)




        open_check = [] # check for parent re-assignment
        if tempList:
            for item in tempList:
                for nodes in openList:
                    if item == nodes.coord:
                        open_check.append(nodes)



        for node in open_check:#needs improvment
            if node.parentNode != None:
                result = findUnitCost(closedList[nodeListIndex],node.coord)
                if node.g > (closedList[nodeListIndex].g + result):
                    print("flag\n\n")
                    node.parentNode = closedList[nodeListIndex]
                    node.g = closedList[nodeListIndex].g + result




        # if walkable already exists check for cheaper path cost
        # else remove duplicte or reassign parent


        #find cost for each walkable [cost 1, cost 2, cost 3... etc
        # cost = [] -> cost = findCost
        costList = findCost(closedList[nodeListIndex].coord,walkable)
        #find heuristic for each walkable [h1, h2,h3... etc.]
        heurisitics = findHeuristic(walkable,goal)
        #pass goal -> tempCoord = h[i]
        # (goal[x] - tempCoord[x]) + (goal[y] - tempCoord[y])

        # append cost and h values
        index = 0
        ChildrenToBeEvaluated = []
        for items in walkable:
            nodeToAppend = newNode(items)
            visited.append(items)

            nodeToAppend.h = heurisitics[index]
            nodeToAppend.g = costList[index] + closedList[nodeListIndex].g
            nodeToAppend.f = heurisitics[index] + costList[index] + closedList[nodeListIndex].g
            nodeToAppend.parentNode = closedList[nodeListIndex]
            openList.append(nodeToAppend)
            ChildrenToBeEvaluated.append(nodeToAppend)
            index += 1
            # set parent
        a = returnArrayByFValue(ChildrenToBeEvaluated)

        if not(a):
            if openList:
                closedList[nodeListIndex] = openList[-1]
                openList.pop(-1)
                continue
            else:
                print("No Solution Found")
                return

        b = a.index(min(a))
        nextParent = ChildrenToBeEvaluated[b]

        #parent node used for path tracing
        #dequeue nextParent from openList

        for items in openList:
            if nextParent.coord == items.coord:
                openList.remove(nextParent)
        nodeListIndex += 1
        closedList.append(nextParent)

        for coords in visited:
            if grid[coords[0]][coords[1]] == 'g':
                print("Goal Found! at " + str(coords[0]) + " " + str(coords[1]) )
                path = traceBack(grid,closedList,startCoordinate)
                for j in path:
                    grid[j[0]][j[1]] = "+"
                grid[startCoordinate[0]][startCoordinate[1]] = "s"
                printGrid(grid)
                return
        u = returnArrayByCoord(closedList)
        os.system("pause");

    # __________________ end loop





def traceBack(grid,nodeList,startCoordinate):
    path = []

    backNode = nodeList[-1].parentNode.coord
    path.append(backNode)

    while backNode != startCoordinate:
        for items in nodeList:
            if items.coord == backNode:
                tempNode = items
                break
        path.append(tempNode.parentNode.coord)
        backNode = tempNode.parentNode.coord

    return path

def searchForWalkable(Coordinate,row,col,grid):

    x = Coordinate[0]
    print(x)
    y = Coordinate[1]
    CoordList = []


    #look right
    tempx = x
    tempy = y+1
    if not(tempy >= col):
        if grid[tempx][tempy] != 'x':
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look left
    tempx = x
    tempy = y-1
    if not(tempy < 0):
        if grid[tempx][tempy] != 'x':
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look up
    tempx = x-1
    tempy = y
    if not(tempx < 0):
        if grid[tempx][tempy] != 'x':
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look down
    tempx = x+1
    tempy = y
    if not(tempx >= row):
        if grid[tempx][tempy] != 'x':
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look upper right
    tempx = x-1
    tempy = y+1
    if not(tempx < 0) and not(tempy >= col):
        if grid[tempx][tempy] != 'x' and  not(grid[x-1][y] == 'x' and grid[x][y+1] == 'x') :
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look upper left
    tempx = x-1
    tempy = y-1
    if not(tempx < 0) and not(tempy < 0):
        if grid[tempx][tempy] != 'x' and  not(grid[x-1][y] == 'x' and grid[x][y-1] == 'x'):
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look bottom left
    tempx = x+1
    tempy = y-1
    if not(tempx >= row) and not(tempy < 0):
        if grid[tempx][tempy] != 'x' and  not(grid[x+1][y] == 'x' and grid[x][y-1] == 'x'):
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)

    #look bottom right
    tempx = x+1
    tempy = y+1
    if not(tempx >= row) and not(tempy >= col):
        if grid[tempx][tempy] != 'x' and  not(grid[x+1][y] == 'x' and grid[x][y+1] == 'x'):
            tempTup = (tempx,tempy)
            CoordList.append(tempTup)
    return CoordList

def findCost(Coordinate,walkable):
    x = Coordinate[0]
    y = Coordinate[1]
    CostList = []
    right = (x,y+1)
    left  = (x,y-1)
    up    = (x-1,y)
    down  = (x+1,y)
    uRight = (x-1,y+1)
    uLeft  = (x-1,y-1)
    bLeft = (x+1,y-1)
    bRight = (x+1,y+1)

    for items in walkable:
        if items == right or items == left or items == up or items == down:
            CostList.append(10)
        else:
            CostList.append(14)
    return CostList

def findUnitCost(ClosedObj, destCoord):
    coord = ClosedObj.coord
    x = coord[0]
    y = coord[1]

    right = (x,y+1)
    left  = (x,y-1)
    up    = (x-1,y)
    down  = (x+1,y)
    uRight = (x-1,y+1)
    uLeft  = (x-1,y-1)
    bLeft = (x+1,y-1)
    bRight = (x+1,y+1)

    if right == destCoord or left == destCoord or up == destCoord or down ==destCoord:
        return 10
    else:
        return 14

def findHeuristic(walkable,goal):

    HeuristicList = []

    for items in walkable:
        r = (goal[1] - items[1])
        if r < 0:
            r = r*(-1)
        t = goal[0] - items[0]
        if t < 0:
            t = t*(-1)
        h = 10*(math.sqrt(pow(r,2)+pow(t,2)))
        h1 = 10*(t+r)
        h2 = 10*(min(abs(t),abs(r)))
        h3 = (h + h1 + h2)/4
        HeuristicList.append(h)



    return HeuristicList

def newNode(tuple):
    newGridNode = GridNode(tuple,True,None,None,0,0,0)
    return newGridNode


def returnArrayByCoord(objectList):
    temp = []
    for object in objectList:
        temp.append(object.coord)
    return temp

def returnArrayByHeuristic(objectList):
    temp = []
    for object in objectList:
        temp.append(object.h)
    return temp
def returnArrayByCost(objectList):
    temp = []
    for object in objectList:
        temp.append(object.g)
    return temp
def returnArrayByFValue(objectList):
    temp = []
    for object in objectList:
        temp.append(object.f)
    return temp

def findStart(grid,row,col):
    i  = j = 0

    for rows in grid:
        for cols in rows:
            if cols == 's':
                return (i,j)
            if j < int(col)-1:
                j += 1
            else:
                j=0
        i += 1


def findGoal(grid,row,col):
    i  = j = 0

    for rows in grid:
        for cols in rows:
            if cols == 'g':
                return (i,j)
            if j < int(col)-1:
                j += 1
            else:
                j=0
        i += 1



def initGridSpace(file,grid,row,col):
    i = 0
    j = 0

    for lines in file:
        for chars in lines.strip("\t").strip("\n").replace(" ",""):
            grid[i][j] = chars
            if j < int(col)-1:
                j += 1
            else:
                j=0
        i += 1
# end init func


def printGrid(grid):
    for rows in grid:
        for cols in rows:
            for chars in cols:
                print(chars,end="")
                print(" ",end="")
        print("\n")
#end printGrid func



#declaration of main function
if __name__ == '__main__':
    main()