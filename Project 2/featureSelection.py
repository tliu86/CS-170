import random

def crossValidation(data, currentSet, addFeature):
    #column 1: 1 or 2 represents what EACH individual 'object' classifies as 
    #k-leave one out: k depends on how many rows there are in the data set 
    #select one 'object' to hide, then try to see if it is correctly classified 
    #accuracy = number of correct classifications/instances in database
    with open(data, "r") as dataFile:
        # accuracy = 0
        rows = dataFile.readlines()
        count = 1

        for instance in rows:
            print(f"Looping over row, at the {count} location")
            print(f"The {count}th object is in the class {instance.strip().split()[0]}")
            count += 1
            # classifiedObject = (instance.strip().split())[1:]
            # print(classifiedObject)


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
