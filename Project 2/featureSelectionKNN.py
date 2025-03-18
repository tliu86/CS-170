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

        for instance in rows: #iterates through each data entry 
            originalClass = instance.strip().split()[0] # specifies what class the instance belongs to 
            ogFeatures = (instance.strip().split())[1:] # looks at the instances' feature values 
            floatOGFeatures = [float(x) for x in ogFeatures] #allows arithmetic operations 

            # print(f"Looping over i, at the {count} location")
            # print(f"The {count}th object is in the class {int(float(originalClass))}")

            nearestNeighborDistance = float('inf')
            nearestNeighborLocation = float('inf')

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
    print(f"Testing accuracy of Feature(s) {testSet}: {numberCorrectClassifed}/{len(rows)} = {accuracy}.")
    return accuracy

#forward feature selection: start off with an empty feature list, identify the BEST feature to add to feature list,
#repeat until ALL features are in the list 
def forwardFeatureSelection(data):
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
                    accuracy = crossValidation(data, currentFeatures, numFeature, 0) #testing only forward selection ATM 

                    '''data = data.txt file, currentFeatures = set of pre-existing features to check,
                    numFeature = the number of the feature to check (shoudl ensure that I PROPERLY look at said feature)'''

                    if accuracy > currentBestAccuracy: #finds the MOST accurate feature given a set of features 
                        currentBestAccuracy = accuracy 
                        featureAdded = numFeature
                
            currentFeatures.add(featureAdded) # adds the MOST accurate feature tested on a given level to the dictionary
            print(f"On level {level}, I added feature {featureAdded} to the current set.")

            if(currentBestAccuracy > globalBestAccuracy):
                globalBestAccuracy = currentBestAccuracy
                globalBestFeatures = globalBestFeatures | currentFeatures
                  
        print(f"The best accuracy acquired is using {globalBestAccuracy * 100}%. And using the set of features {globalBestFeatures}")

if __name__ == "__main__":
    # forwardFeatureSelection('CS170_Small_Data__94.txt')
    forwardFeatureSelection('CS170_Large_Data__71.txt')
