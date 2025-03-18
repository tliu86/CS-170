import math

def crossValidation(data, currentFeatures, addFeature, typeOfFeatureSelection):
    #column 1: 1 or 2 represents what EACH individual 'object' classifies as 
    #k-leave one out: k depends on how many rows there are in the data set 
    #select one 'object' to hide, then try to see if it is correctly classified 
    with open(data, "r") as dataFile:

        rows = dataFile.readlines() 
        numberCorrectClassifed = 0
        count = 0

        if(typeOfFeatureSelection == 0): #choose forward selection
            testSet = currentFeatures | {addFeature} #temporary set of the DESIRED FEATURES to look at 
        elif(typeOfFeatureSelection == 1): #choose backward elimination
            testSet = currentFeatures ^ {addFeature}
        else: 
            print("Something horrific happened")
            return 0

        for instance in rows: #iterates through each data entry 
            originalClass = instance.strip().split()[0] # specifies what class the instance belongs to 
            ogFeatures = (instance.strip().split())[1:] # looks at the instances' feature values 
            floatOGFeatures = [float(x) for x in ogFeatures] #allows arithmetic operations 

            # print(f"Looping over i, at the {count} location")
            # print(f"The {count}th object is in the class {int(float(originalClass))}")

            nearestNeighborDistance = float('inf')
            # nearestNeighborLocation = float('inf')

            count += 1 #identifies what entry is being tested 

            for k in range(0, len(rows)): #iterates from 0-len(rows) --> accesses all possible entries (rows) 
                if k+1 != (count): #prevents an instance from checking against itself 
                    # print(f"Ask if {count} is nearest neighbor with {k}")
                    testNeighbor = rows[k].strip().split()[1:] 
                    floatTestNeighbor = [float(x) for x in testNeighbor] #allows arithmetic operations

                    indSquaredDistance = []
                    pairedInstances = zip(floatOGFeatures, floatTestNeighbor)

                    featureCounter = 0
                    for x, y in pairedInstances: #looks at features between an instance and a different instance
                        if featureCounter+1 in testSet: #filters only the specific features to look at
                            # print(f"Looking at Feature {featureCounter} given these features activated {currentFeatures}.") 
                            squaredDiff = (x - y) ** 2
                            indSquaredDistance.append(squaredDiff)

                        featureCounter += 1 #lets me iterate through each independent feature 

                    sumOfSquaredDistances = sum(indSquaredDistance)
                    distance = math.sqrt(sumOfSquaredDistances)

                    # distance = math.sqrt(sum([(x - y) ** 2 for x, y in zip(floatOGFeatures, floatTestNeighbor)])) # one-liner

                    if distance < nearestNeighborDistance:
                        nearestNeighborDistance = distance
                        nearestNeighborLocation = k
                        nearestNeighborClassLabel = rows[k].strip().split()[0] #class label of the 'updated' nearest neighbor 
                    # print(f"Ask if {count} is nearest neighbor with {k}; the distance is {distance}")

            # print(f"Object {count} is of ORIGINAL class {originalClass}")
            # print(f"It's nearest neighbor is {nearestNeighborLocation} which is in class {nearestNeighborClassLabel}")
            if originalClass == nearestNeighborClassLabel:
                numberCorrectClassifed += 1

    accuracy = numberCorrectClassifed / len(rows)
    print(f"The accuracy of feature(s) {testSet}: {(accuracy * 100):.1f}%.") #note on backward elimination: if empty set --> assumes class of 1st entry ! (small__94 --> 93/500)
    return accuracy

#forward feature selection: start off with an empty feature list, identify the BEST feature to add to feature list,
#repeat until ALL features are in the list 
def forwardFeatureSelection(data, typeOfFeatureSelection):
    globalBestAccuracy = 0
    globalBestFeatures = set()

    with open(data, "r") as dataFile:
        firstLine = dataFile.readline().strip()  
        columns = firstLine.split() #identify the column values: column 1 --> class identification, column 2 and ONWARD --> different features 
        currentFeatures = set()
        
        #number of levels = number of features 
        for level in range(1, len(columns)): #iterate through all possible levels in the provided data.txt file 
            print(f"\nOn the {level}th level of the search tree:")
            featureAdded = 0
            currentBestAccuracy = 0

            for numFeature in range(1, len(columns)): #iterate through all possible features in the provided data.txt file
                if numFeature not in currentFeatures: #checks all VALID features 
                    # print(f"Considering adding feature {numFeature}")
                    accuracy = crossValidation(data, currentFeatures, numFeature, typeOfFeatureSelection) 

                    '''data = data.txt file, currentFeatures = set of pre-existing features to check,
                    numFeature = the number of the feature to check (shoudl ensure that I PROPERLY look at said feature)'''

                    if accuracy > currentBestAccuracy: #finds the MOST accurate feature given a set of features 
                        currentBestAccuracy = accuracy 
                        featureAdded = numFeature
                
            currentFeatures.add(featureAdded) # adds the MOST accurate feature tested on a given level to the dictionary
            print(f"\nOn level {level}, I added feature {featureAdded} to the current set. The current set is now {currentFeatures} with an accuracy of {(currentBestAccuracy * 100):.1f}%.")

            if(currentBestAccuracy > globalBestAccuracy):
                globalBestAccuracy = currentBestAccuracy
                globalBestFeatures = globalBestFeatures | currentFeatures
                  
        print(f"The BEST set of feature(s) is {globalBestFeatures} with an accuracy of {(globalBestAccuracy * 100):.1f}%.")

#backward feature elimination: start off with an FULL feature list, identify the WORST feature and remove from the feature list,
#repeat until ALL features gone from list 
def backwardFeatureElimination(data, typeOfFeatureSelection):
    globalBestAccuracy = 0
    globalBestFeatures = set()

    with open(data, "r") as dataFile:
        firstLine = dataFile.readline().strip()  
        columns = firstLine.split() #identify the column values: column 1 --> class identification, column 2 and ONWARD --> different features 
        currentFeatures = set() 

        for feature in range(1, len(columns)): #initializes with all possible features 
            currentFeatures.add(feature) 
   
        for level in range(1, len(columns)): #iterate through all possible levels in the provided data.txt file 
            print(f"\nOn the {level}th level of the search tree:")
            featureRemoved = 0
            currentBestAccuracy = 0

            for numFeature in range(1, len(columns)): #iterate through all possible features in the provided data.txt file
                if numFeature in currentFeatures: #checks all VALID features 
                    # print(f"Considering removing feature {numFeature}")
                    accuracy = crossValidation(data, currentFeatures, numFeature, typeOfFeatureSelection) 

                    if accuracy > currentBestAccuracy: #the higher the accuracy means the more misleading a feature is --> must remove
                        currentBestAccuracy = accuracy 
                        featureRemoved = numFeature
                
            currentFeatures = currentFeatures ^ {featureRemoved} # removes the WORST feature tested on a given level
            print(f"\nOn level {level}, I removed feature {featureRemoved} from the current set. The current set is now {currentFeatures} with an accuracy of {(currentBestAccuracy * 100):.1f}%.")

            if(currentBestAccuracy > globalBestAccuracy):
                globalBestAccuracy = currentBestAccuracy
                globalBestFeatures = currentFeatures.copy()
                  
        print(f"The BEST set of feature(s) is {globalBestFeatures} with an accuracy of {(globalBestAccuracy * 100):.1f}%.")

if __name__ == "__main__":

    print("You have entered the Searching Zone!")
    data = input("Type in the name of the file you want to test: ")
    typeOfFeatureSelection = int(input("Type the number of the algorithm you want to run.\n     0) Forward Selection\n     1) Backward Eliminiation\n"))

    if(typeOfFeatureSelection > 1 or typeOfFeatureSelection < 0):
        print("Invalid number to select algorithm")
    else: 
        if typeOfFeatureSelection == 0: #forward selection
            forwardFeatureSelection(data, typeOfFeatureSelection)
        elif typeOfFeatureSelection == 1: #backward elimination 
            backwardFeatureElimination(data, typeOfFeatureSelection)
        else:
            print("Something horrific happened.")

    # forwardFeatureSelection('CS170_Small_Data__94.txt')
    # forwardFeatureSelection('CS170_Large_Data__71.txt')