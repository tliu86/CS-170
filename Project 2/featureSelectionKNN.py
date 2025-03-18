import random
import math

#TO-DO: 
# identify which features to look at --> must look at currentSet and addFeature --> ignore ALL other features 
# set those 'ignored features' to 0 

def crossValidation(data, currentSet, addFeature, typeOfFeatureSelection):
    #column 1: 1 or 2 represents what EACH individual 'object' classifies as 
    #k-leave one out: k depends on how many rows there are in the data set 
    #select one 'object' to hide, then try to see if it is correctly classified 
    with open(data, "r") as dataFile:

        rows = dataFile.readlines() 
        numberCorrectClassifed = 0
        count = 0

        #should try to 0 out values looking at BEFORE the nested for loops:
        #make a copy of the data.txt? --> HECK NO THATS TOO SLOW
        #only look at currentSet AND the desiredFeature

        if(typeOfFeatureSelection == 0): #choose forward selection
            testSet = currentSet.add(addFeature) #temporary set of the DESIRED FEATURES to look at 

        for instance in rows: #iterates through each data entry 
            originalClass = instance.strip().split()[0] # specifies what class an instance belongs to 
            ogFeatures = (instance.strip().split())[1:] # looks at a particular instances' feature values 

            floatOGFeatures = [float(x) for x in ogFeatures] 
            # print(f"Looping over i, at the {count} location")
            # print(f"The {count}th object is in the class {int(float(originalClass))}")

            nearestNeighborDistance = float('inf')
            nearestNeighborLocation = float('inf')

            count += 1
            for k in range(1, len(rows)+1): #do i need +1 to len(rows)? 
                if k != (count):
                    # print(f"Ask if {count} is nearest neighbor with {k}")
                    testNeighbor = rows[k-1].strip().split()[1:] #in the txt file we pulled from, the rows are indexed by k-1
                    floatTestNeighbor = [float(x) for x in testNeighbor]
                    
                    distance = math.sqrt(sum([(x - y) ** 2 for x, y in zip(floatOGFeatures, floatTestNeighbor)]))

                    if distance < nearestNeighborDistance:
                        nearestNeighborDistance = distance
                        nearestNeighborLocation = k
                        nearestNeighborClassLabel = rows[k-1].strip().split()[0] #class label of the 'updated' nearest neighbor 
                    

                    # print(f"Ask if {count} is nearest neighbor with {k}; the distance is {distance}")

            # print(f"Object {count} is of ORIGINAL class {originalClass}")
            # print(f"It's nearest neighbor is {nearestNeighborLocation} which is in class {nearestNeighborClassLabel}")
            if originalClass == nearestNeighborClassLabel:
                numberCorrectClassifed += 1

        accuracy = numberCorrectClassifed / len(rows)
    print(f"Testing accuracy: {accuracy}")
    # return accuracy 

    #figure out how to validate, after checking then call search. 
    # print(addFeature)
    return random.randint(1, 100)

#forward feature selection: start off with an empty feature list, identify the BEST feature to add to feature list,
#repeat until ALL features are in the list 
def forwardFeatureSelection(data):
    #IEEE format! (convert at some point in time)

    with open(data, "r") as dataFile:
        firstLine = dataFile.readline().strip()  
        columns = firstLine.split() #identify the column values: column 1 --> class identification, column 2 and ONWARD --> different features 
        currentFeatures = {} 
        
        #number of levels = number of features 
        for level in range(1, len(columns)): #iterate through all possible levels in the provided data.txt file 
            print(f"\nOn the {level}th of the search tree")
            featureAdded = 0
            currentBestAccuracy = 0

            for numFeature in range(1, len(columns)): #iterate through all possible features in the provided data.txt file
                if numFeature not in currentFeatures: #checks all VALID features 
                    print(f"Considering adding feature {numFeature}")
                    accuracy = crossValidation(data, currentFeatures, numFeature) 
                    '''data = data.txt file, currentFeatures = set of pre-existing features to check,
                    numFeature = the number of the feature to check (shoudl ensure that I PROPERLY look at said feature)'''

                    if accuracy > currentBestAccuracy: #finds the MOST accurate feature given a set of features 
                        currentBestAccuracy = accuracy 
                        featureAdded = numFeature
                
            currentFeatures.add(featureAdded) # adds the MOST accurate feature tested on a given level to the dictionary
            print(f"On level {level}, I added feature {featureAdded} to the current set")

if __name__ == "__main__":
    # print(crossValidation(1, 2, 3))
    forwardFeatureSelection('CS170_Small_Data__94.txt')
