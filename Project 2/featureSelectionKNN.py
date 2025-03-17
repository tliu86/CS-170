import random
import math

def crossValidation(data, currentSet, addFeature):
    #column 1: 1 or 2 represents what EACH individual 'object' classifies as 
    #k-leave one out: k depends on how many rows there are in the data set 
    #select one 'object' to hide, then try to see if it is correctly classified 
    #accuracy = number of correct classifications/instances in database
    with open(data, "r") as dataFile:

        rows = dataFile.readlines()
        numberCorrectClassifed = 0
        count = 0

        for instance in rows:
            originalClass = instance.strip().split()[0] # file specifies what class a feature belongs to 
            ogFeatures = (instance.strip().split())[1:] # looks at the feature columns 
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
                    # indSquaredDistance = [(x - y) ** 2 for x, y in zip(floatOGFeatures, floatTestNeighbor)]
                    # sumOfSquaredDistances = sum(indSquaredDistance)
                    # distance = math.sqrt(sumOfSquaredDistances)

                    # can combine into one line 
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

def featureSelection(data):
    #data -- data set file 
    #walk down all the levels (of features)
    #1st column: class label --> will either be 1 or 2 
    #rest of columns: depict features --> positive or negative, big or small 
    #IEEE format! (convert at some point in time)

    with open(data, "r") as dataFile:
        firstLine = dataFile.readline().strip()
        columns = firstLine.split()
        currentFeatures = {}

        for level in range(1, len(columns)):
            print(f"\nOn the {level}th of the search tree")
            featureAdded = 0
            currentBestAccuracy = 0

            for numFeature in range(1, len(columns)):
                if numFeature not in currentFeatures:
                    print(f"Considering adding feature {numFeature}")
                    accuracy = crossValidation(data, currentFeatures, numFeature+1) #k+1 to ensure the proper column is looked at as 1st column is NOT a feature

                    if accuracy > currentBestAccuracy:
                        currentBestAccuracy = accuracy 
                        featureAdded = numFeature
                
            currentFeatures[featureAdded] = 1
            print(f"On level {level}, I added feature {featureAdded} to the current set")

if __name__ == "__main__":
    # print(crossValidation(1, 2, 3))
    featureSelection('CS170_Small_Data__94.txt')
