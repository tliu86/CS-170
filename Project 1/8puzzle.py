def aStar():
    #code A* 
    print("test")

def heuristic(option):
    if option == 0:
        return 0
    elif option == 1: 
        return misplacedTile()
    elif option == 2: 
        return manhattanDistance()
    else:
        raise ValueError("Invalid heuristic selected")

def misplacedTile():
    #uses misplacedTile heuristic 
    print("hi")

def manhattanDistance():
    #uses manhattanDistance heuristic
    print("ok")

if __name__ == "__main__":
    goalState = [
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]
    
    # print(goalState)