#modDataSummary.py
from itertools import groupby

#Summarize will take a dictionary, and a key name from that dictionary
#It will return a list of summed keys based on that data
def Summarize(ds1, col1):
    
    retVal = {}
    #First we need to sort the list
    newList = sorted(ds1, key=lambda k: k[col1])

    gb = groupby(newList, lambda item: item[col1])

    for key, group in gb:
        #retVal[key] = len([item[col1] for item in group])
        retVal[key] = len(list(group))

    return retVal





def Summarize2D(ds1, col1, col2, col1List=None, col2List = None):

    retVal = {}

    #
    #for key in col1List:
        
    #    subRetVal = {}
    #    for key2 in col2List:
    #        subRetVal[key2] = 0
    #    retVal[key] =  subRetVal

    

    #First we need to sort the list
    newList = sorted(ds1, key=lambda k: k[col1])

    #Then some basic grouping
    gb = groupby(newList, lambda item: item[col1])

    #Iterate through the first group
    for c1key, group in gb:
        newList2 = sorted(list(group), key=lambda k: k[col2])
        
        
        #retVal[key] = Summarize(newList2, col2)
        
        sum1 = Summarize(newList2, col2)
        for c2key in sum1.keys():
            #Setup a basic dictionary if one does not exist yet
            if (c1key not in retVal.keys()):
                retVal[c1key] = {}
            
            retVal[c1key][c2key] = sum1[c2key]
        
        
        #gb2 = groupby(gb, lambda item: item[col2])
        #retVal[key] = len([item[col2] for item in group])

    return retVal
    
