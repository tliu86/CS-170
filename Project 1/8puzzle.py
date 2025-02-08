import heapq

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

    def search():
        #searching
        print("search")

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
    
    def toString(self, current):
        return " # ".join(" ".join(str(tile) for tile in row) for row in current)

if __name__ == "__main__":
    depth0 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    depth2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    depth4 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
    depth8 = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
    depth12 = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
    depth16 = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
    depth20 = [[7, 1, 2], [4, 8, 5], [6, 3, 0]]
    depth24 = [[0, 7, 2], [4, 6, 1], [3, 5, 8]]

    eightPuzzle = Puzzle(3, depth8)
    print(eightPuzzle.manhattanDistance(depth8))
    print(eightPuzzle.misplacedTile(depth8))
    print(eightPuzzle.toString(depth8))
    # print(eightPuzzle.goalState)