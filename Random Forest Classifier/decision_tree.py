from util import entropy, information_gain, partition_classes
import numpy as np 
import ast
import operator


class DecisionTree(object):
    def __init__(self):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = {}

    def learn(self, X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)

        def sortLast(y):
            classCount={}
            for vote in y:
                if vote not in classCount.keys():
                    classCount[vote] = 0
                    classCount[vote] += 1
            sortedClassCount = sorted(classCount.iteritems(),
                              key = operator.itemgetter(1), reverse=True)
            return sortedClassCount[0][0]

        def chooseBestFeatureToSplit(X, y):
            numFeatures = len(X[0])
            bestInfoGain = 0.0
            bestFeature = -1
            bestValue = 0
            for i in range(numFeatures):
                featList = [example[i] for example in X]
                uniqueVals = set(featList)
                for value in uniqueVals:
                    yl = partition_classes(X, y, i, value)[2]
                    yr = partition_classes(X, y, i, value)[3]
                    cy = [yl, yr]
                    infoGain = information_gain(y, cy)
                    if (infoGain > bestInfoGain):
                        bestInfoGain = infoGain
                        bestFeature = i
                        bestValue = value
            return bestFeature, bestValue

        def creatTree(X, y):
            # m, n is the number of line and column
            m, n = X.shape
            # all the label is the same
            if y.count(y[0]) == len(y):
                return y[0]
            # only one feature(column) left
            if n == 1:
                return sortLast(y)  # classify them as one class
            # bestFeat is the column index of feature
            # bestVal is the classify value in that column
            bestFeat, bestVal = chooseBestFeatureToSplit(X, y)
            myTree = {bestFeat: {}}
            Xl = partition_classes(X, y, bestFeat, bestVal)[0]
            yl = partition_classes(X, y, bestFeat, bestVal)[1]
            Xr = partition_classes(X, y, bestFeat, bestVal)[2]
            yr = partition_classes(X, y, bestFeat, bestVal)[3]
            myTree[bestFeat]["<=" + str(bestVal)] = creatTree(Xl, yl)
            myTree[bestFeat][">" + str(bestVal)] = creatTree(Xr, yr)
            return myTree

        self.tree = creatTree(X, y)

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        myTree = self.tree
        while myTree != "0" and myTree != 1:
            feature = myTree.keys()[0]
            value = float(record[feature])
            myTree = myvalue[feature]
            myValueString = myTree.keys()[0]
            if ">" in myValueString:
                myvalue = float(myValueString[1:])
                if value <= myvalue:
                    myTree = myTree[myTree.keys()[1]]
                else:
                    myTree = myTree[myTree.keys()[0]]
            else:
                myvalue = float(myValueString[2:])
                if value <= myvalue:
                    myTree = myTree[myTree.keys()[1]]
                else:
                    myTree = myTree[myTree.keys()[0]]
        return int(myTree)



