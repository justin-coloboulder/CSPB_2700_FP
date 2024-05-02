# Decision Tree Implementation
CSPB-2700 Final Project

Justin Reid

## Overview
For my project I implemented and tested a decision tree structure in Python. I used a publicly available dataset related to health metrics and drug prescriptions. I used part of the dataset to build the decision tree, and then used the tree to predict which drug was prescriped to the remaining persons represented in the data. Finally, I implemented simple system for testing this process repeatedly to determine its average accuracy and then visualize the distribution of the % correct predictions. 

## Classes
Generally, decision trees utilize two separate node types, 1) a decision node, which contains a "test" that determines which proceeding node is checked, and a leaf node that contains data that has been separated based on the decision nodes. For example, in my dataset one level of nodes may contain tests for the "blood pressure" attribute (which has values of "low", "medium" and "high"). In predicting the drug recieved by some unknown patient, the node represents the value matching the unknown patient value will be visited. The children of that decision node will contain tests for another attribute, and that process will repeat until finally a leaf node is reached, which contain no test and only the value(s) of interest (i.e. the prescribed drug)

While writing the program, I found that I was easily able to omit the leaf node class. I explain this in the video, but I found that I had accomplished the prediction process without utilizing leaf nodes explicitly and was writing extra code to create and evaluate leaf nodes. I decided that was unecessary for my purpose. There are probably drawbacks to that choice I am not considering, but I cannot think of any in the context of this project. Instead, terminal decision nodes are identified by the absence of child nodes, which is effectively a leaf node. 

## Tree-Building Functions

### calculateEntropy()
The decision tree algorithm builds the decision tree by iteratively selecting the attribute that 1) best segragates the value of interest (the drug) and 2) has not previously been used to segragate the data. The attribute that best segragates the data is determined by the entropy of the child nodes that are created based on separate the data by that attribute. Nodes that have more "pure" data (in this case, more consistent drug prescriptions) have lower entropy and the attribute that produces data with the lowest entropy is selected. 

This function takes data stored from the parent node, an attribute, calculates the weighted entropy of each child node. The weighted entropy value is returned by the function and used in another tree-building function. 

### findBestAttribute()
This function iterates through all attributes, separating data and calculating the entropy of child nodes using calculateEntropy(). The attribute that results in the lowest entropy value is returned. 

### makeAttributeNodes()
The purpose of this function is to make the child nodes based on the "best" attribute. The function iterates through each unique value of the attribute, making new nodes that contain data that is subsetted based on the presence of that value. 

### BuildTree()
This function takes the root node as a parameter. It then builds the decision tree using the functions described above. 

## Data Processing
First, the .csv containing the data is imported. The data contains two continuous values, "Na_to_K" and "Age" which must be discretized. I used the pandas.qcut() function to accomplish this and added labels to "Age". I also stored the attributes in an array, as those values are used in the buildTree() function. 

Next, the root node is created as a decision node that contains all attributes and data. Then, the tree is built starting at the root node. 

## Data-Searching Functions

### probeNode()
Takes one item of test data and compares its value of the attribute stored in the node versus the value stored in the node. If the test data and node values match, the node is visited. Returns true or false depending on whether the values match. 

### iterateNodes()
Iterates across a set of child nodes, using probeNodes() to determine which node should be visited. Nodes are visited iteratively until a "leaf" node is reached (i.e. a node without children). Once the leaf node is visited, the "Drug" value stored at that node is determined, representing the prediction. 

## Prediction Evaluation
Finally, the tree-building and prediction-making process is tested 100 times. Training and test data is subsetted randomly each time, so each test of the algorithm is presumably unique. The relative accuracy of the prediction for each tree/test combination is stored in an array.The values in the array are then visualized using a simple histogram made using matplot. 

## Conclusion
The prediction accuracy was quite high, generally from 92.0-98.0%. This is not very surprsing considering this dataset was apparently designed for implementing this particular structure. Although the above is not particularly interesting to consider, it does show that the algorithm functions correctly for this particular dataset. 

## Dataset Citation

jeevanrh. (2020). *Drug200.csv*. Kaggle. https://www.kaggle.com/datasets/jeevanrh/drug200csv
