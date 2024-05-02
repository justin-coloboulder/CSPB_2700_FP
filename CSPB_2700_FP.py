import os
import numpy
import pandas as pd
import matplotlib.pyplot as plt

#Node Classes
class decisionNode:
    def __init__(self, data):
        self.attribute = None
        self.test = None
        self.featurecols = []
        self.data = data
        self.childNodes = []

#Algorithm Functions 
# Calculate entropy
def calculateEntropy(data, testAttribute, evalAttribute):
    uniqueValues = data[testAttribute].unique()
    numberAllValues = data.shape[0]
    weightedEntropy = 0
    for value in uniqueValues:
        subData = data.loc[data[testAttribute] == value]
        numberSubVals = subData.shape[0]
        frequencies = data[evalAttribute].value_counts() / numberSubVals
        entropies = frequencies * numpy.log2(frequencies)

        averageEntropy = 0
        for ent in entropies:
            averageEntropy = averageEntropy - ent
        weightedEntropy = weightedEntropy + (averageEntropy * (numberSubVals / numberAllValues))
    
    return(weightedEntropy)

# Find attribute -> lowest entropy after split 
def findBestAttribute(data, testAttributes, evalAttributes):
    bestAttribute = None
    bestEntropy = 10000
    for attribute in testAttributes:
        curEntropy = calculateEntropy(data, attribute, evalAttributes)
        if curEntropy < bestEntropy:
            bestEntropy = curEntropy
            bestAttribute = attribute
    return(bestAttribute)

# Make nodes based on attributes
def makeAttributeNodes(parentnode, data, attribute):
    uniqueValues = data[attribute].unique()
    parentFeatureCols = parentnode.featurecols
    for value in uniqueValues:
        subData = data.loc[data[attribute] == value]
        curNode = decisionNode(subData)
        curNode.attribute = attribute
        curNode.test = value
        #Remove the feature since is has been used
        curNode.featurecols = parentFeatureCols.copy()
        curNode.featurecols.remove(attribute)
        parentnode.childNodes.append(curNode)
        

#Build Tree
def buildTree(startnode):
    curNode = startnode
    if(len(curNode.featurecols) > 1):
        for node in curNode.childNodes:
            curBestAttribute = findBestAttribute(node.data, node.featurecols, "Drug")
            makeAttributeNodes(node, node.data, curBestAttribute)
            buildTree(node)
            
# Get the directory of the current Python script
script_directory = os.path.dirname(os.path.abspath(__file__))
# Change the current working directory to the script directory
os.chdir(script_directory)
#Read in wine quality .csv
drugData = pd.read_csv("drug200.csv")

#Subsetting data 
#["Age", "Sex", "BP", "Cholesterol", "Na_to_K"]
#Bin values in "NA_to_K" and "Age" columns 
drugData["Na_to_K"] = pd.qcut(drugData["Na_to_K"], q=5, labels = False)
drugData["Age"] = pd.qcut(drugData['Age'], q=3, labels=['Younger', 'Middle', 'Older'])
featureColumns = ["Age", "Sex", "BP", "Cholesterol", "Na_to_K"]
numRows = drugData.shape[0]

#Initialize root node (contains entire df) and create child nodes
rootNode = decisionNode(drugData)
rootNode.featurecols = featureColumns
curBestAttribute = findBestAttribute(drugData, featureColumns, "Drug")
makeAttributeNodes(rootNode, rootNode.data, curBestAttribute)
#Now all child nodes in root nodes contain data
buildTree(rootNode)

def probeNode(testdata, node, attribute):
    testValue = testdata[attribute]
    nodeValue = node.data[attribute].unique()
    if testValue == nodeValue:
        return(True)
    else:
        return(False)

def iterateNodes(testdata, node, idattribute):
    if(len(node.childNodes) == 0):
        correctID = (testdata[idattribute] == node.data[idattribute].mode().iloc[0])
        if correctID == True:
            return True
        else:
            return False
    else:
        for i in range(len(node.childNodes)):
            if(probeNode(testdata, node.childNodes[i], node.childNodes[i].attribute)):
                foundNode = node.childNodes[i]
                return iterateNodes(testdata, foundNode, idattribute)


correctEvalsList = []

for j in range(100):

    #Separate into training and test sets
    trainingData = drugData.sample(frac = 0.75)
    testData = drugData.drop(trainingData.index)
    
    numEvaluations = testData.shape[0]
    numCorrectEvals = 0

    #Initialize root node (contains entire df) and create child nodes
    rootNode = decisionNode(drugData)
    rootNode.featurecols = featureColumns
    curBestAttribute = findBestAttribute(drugData, featureColumns, "Drug")
    makeAttributeNodes(rootNode, drugData, curBestAttribute)
    #Now all child nodes in root nodes contain data
    buildTree(rootNode)

    for i in range(testData.shape[0]):
        correctId = iterateNodes(testData.iloc[i], rootNode, "Drug")
        if(correctId == True):
            numCorrectEvals += 1
    proportionCorrect = numCorrectEvals/numEvaluations * 100
    correctEvalsList.append(proportionCorrect)

average = sum(correctEvalsList)/len(correctEvalsList)

plt.hist(correctEvalsList, align= "mid")
plt.xlabel("Succesful Drug Identification in 25 Attempts (%)")
plt.xlabel("Frequency")
plt.title("Successful Identification - 100 Runs, Average = " + str(average))
plt.show()


