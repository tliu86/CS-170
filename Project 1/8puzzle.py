import heapq
import copy

class Puzzle:
    def __init__(self, dimensions, initState):
        self.dimensions = dimensions
        self.size = dimensions * dimensions
        self.initState = initState 
        self.goalState = self.createGoalState()

    def createGoalState(self):
        goalState = []
        for i in range(self.dimensions):
            row = []
            for j in range(self.dimensions):
                if not (i == self.dimensions-1 and j == self.dimensions-1):
                    row.append(i*self.dimensions + j + 1)
                else:
                    row.append(0)
            goalState.append(row)
        return goalState

    def search(self, heuristicChoice):
        heap = []
        previous = {}
        traversed = set()
        nodesExpanded = 0
        maxFrontier = 0 #number of nodes in frontier will be maxFrontier-1 

        heapq.heappush(heap, (0, self.initState))
        # print(f"Initially: {self.initState}")

        gValue = {self.toString(self.initState): 0}
        hValue = {self.toString(self.initState): self.heuristic(heuristicChoice, self.initState)}

        while heap:
            if nodesExpanded > 50000: #chosen limit for nodesExpanded (any longer I presume as FAILED)
                print("Search failed.")
                return
            
            maxFrontier = max(maxFrontier, len(heap))
            cost, current = heapq.heappop(heap)
            currentString = self.toString(current)
            # tracePrint(current, gValue[currentString], hValue[currentString]) #comment out to not see ALL expanded nodes
            traversed.add(currentString)
            nodesExpanded += 1

            if current == self.goalState:
                solution = []
                while currentString in previous:
                    solution.append(current)
                    currentString = previous[currentString]
                    current = self.fromString(currentString)
                solution.append(self.initState)
                solution.reverse()

                print("Ideal Solution:")
                depth = formatPuzzle(solution)
                print(f"Depth: {depth}")
                print(f"Expanded Nodes: {nodesExpanded}")
                print(f"Frontier Nodes in Queue: {maxFrontier-1}/{maxFrontier}")
                return #successfully obtained path from initial state to goal state 
            
            for move in self.potentialMoves(current):
                moveString = self.toString(move)
                moveCost = gValue[currentString] + 1
                if moveString not in traversed:
                    if moveString not in previous or moveCost < gValue[moveString]:
                        previous[moveString] = currentString
                        gValue[moveString] = moveCost
                        hValue[moveString] = self.heuristic(heuristicChoice, move)
                        heapq.heappush(heap, (gValue[moveString] + hValue[moveString], move))
                    # else:
                    #     #bad things happened 
                    #     raise ValueError("Update to queue failed.")


    def misplacedTile(self, current):
        misplaced = 0 
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                if current[i][j] != self.goalState[i][j] and current[i][j] != 0:
                    misplaced += 1
        return misplaced

    def manhattanDistance(self, current):
        distance = 0 
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                if current[i][j] != 0:
                    goalRow = (current[i][j] - 1)//self.dimensions
                    goalColumn = (current[i][j] - 1)%self.dimensions
                    distance += abs(goalRow - i) + abs(goalColumn - j)
        return distance

    def heuristic(self, option, current):
        if option == 0:
            return 0
        elif option == 1: 
            return self.misplacedTile(current)
        elif option == 2: 
            return self.manhattanDistance(current)
        else:
            raise ValueError("Invalid heuristic selected")
        
    def potentialMoves(self, current):

        allowedMoves = []
        for i in range(self.dimensions):
            for j in range(self.dimensions):
                if current[i][j] == 0:
                    blank = f"{i} {j}"

        rBlank = int(blank[0])
        cBlank = int(blank[2])

        if(rBlank > 0):
            allowedMoves.append(self.swap(current, rBlank, cBlank, rBlank-1, cBlank))
        if(rBlank < self.dimensions-1):
            allowedMoves.append(self.swap(current, rBlank, cBlank, rBlank+1, cBlank))
        if(cBlank > 0):
            allowedMoves.append(self.swap(current, rBlank, cBlank, rBlank, cBlank-1))
        if(cBlank < self.dimensions-1):
            allowedMoves.append(self.swap(current, rBlank, cBlank, rBlank, cBlank+1))
        
        return allowedMoves

    def swap(self, current, r1, c1, r2, c2):
        tempState = copy.deepcopy(current) #if tempState = current, current would ALSO get modified 
        tempState[r1][c1] = current[r2][c2]
        tempState[r2][c2] = current[r1][c1]
        return tempState
    
    def toString(self, current):
        return " # ".join(" ".join(str(tile) for tile in row) for row in current)
    
    def fromString(self, currentString):
        rows = currentString.split(" # ")
        state = []
        for row in rows:
            state.append([int(tile) for tile in row.split()])
        return state
    
def tracePrint(current, baseCost, heuristicCost):
    print(f"The best state to expand with a g(n) = {baseCost} and h(n) = {heuristicCost} is...")
    for row in current:
        print(row)
    print()
    
def formatPuzzle(answer):
    moves = 0
    for row in answer:
        print(f"Move {moves}:")
        for value in row:
            print(f"{value} ")
        moves += 1
        print()
    return moves-1 #don't want to include the initial state as part of the depth 


if __name__ == "__main__":
    #Hardcoded: 8 puzzle examples, taken from Project 1 instructions 
    depth0 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    depth2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    depth4 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
    depth8 = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
    depth12 = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
    depth16 = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
    depth20 = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
    depth24 = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]

    #Additional hardcoded: examples taken from https://deniz.co/8-puzzle-solver/
    easy =  [[1, 5, 2], [4, 0, 3], [7, 8, 6]] #depth of 4 
    hard = [[1, 7, 0], [5, 4, 3], [6, 2, 8]] #depth of 22 

    #Determine what puzzle will be solved 
    userChoice = int(input("Choose 1 to use a hardcoded puzzle or choose 2 to specifically input a puzzle: "))
    if(userChoice == 1):
        puzzle = Puzzle(3, depth24) #just changing to hardcoded examples above, no switch statement  
        # print("Using A* Manhattan Distance Search:\n")
        # puzzle.search(2) 
        
        for i in range(3):
            if i == 0:
                search = "Uniform Cost Search: "
            elif i == 1: 
                search = "A* with Displaced Tile: "
            else:
                search = "A* with Manhattan Distance: "

            print(f"{search}\n")
            puzzle.search(i)
            print()

    elif(userChoice == 2):
        userDimensions = int(input("Enter the dimensions of the puzzle: "))
        userInitState = []

        for i in range(userDimensions):
            userRow = []
            for j in range(userDimensions):
                userNums = int(input(f"Enter value for row {i} column {j}: "))
                userRow.append(userNums)
            userInitState.append(userRow)

        userPuzzle = Puzzle(userDimensions, userInitState)
        searchAlgo = int(input("Enter (1) for Uniform Cost Search, enter (2) for A* with Displace Tile Heuristic, and enter (3) for A* with Manhattan Distance Heuristic"))
        userPuzzle.search(searchAlgo)
    else:
        print("Invalid selection")

