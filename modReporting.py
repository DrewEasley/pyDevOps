#modReporting




def newReport():
    reportData = {}
    return reportData




#Possibly options include widthType=[MAX, AVERAGE]
#maxIters is the number of data points to take from the list
#TODO: Take random samples instead of the first 200
def setColumnWidth(data, maxIters = 200, widthType = "MAX"):


    #If data is an INTEGER, return it as the columnWidth
    if (type(data) == (type(2))):
        return data

    #If data is a STRING, return the string length as columnWidth
    if (
            type(data) == type("MyString") or 
            type(data) == type(u"MyString")
        ):
        return len(data)

    #If data is a list (most likely case)
    if (type (data) == type([])):
        #Cut the data to our sample size
        if (len(data) > maxIters):
            data = data[:maxIters]
        else:
            data = data


        colSum = 0
        colMax = 0
        itemErrors = 0
        
        for it in data:

            try:
                itemLength = len(it)
            except:
                itemLength = 0
                itemErrors = itemErrors + 1

            colSum = colSum + itemLength
            if (itemLength > colMax):
                colMax = itemLength

        colAvg = colSum / (len(data) - itemErrors) # Average columnLength

        if (widthType.upper() == "AVERAGE"):
            return colAvg
        if (widthType.upper() == "MAX"):
            return colMax
        else:
            return colMax

    #Other data types:
    try:
        return len(data)

    except:
        return None #Return no length if we cannot properly calulate this

        
def SlickGridOptions(Editable = False, AllowAdd=False, AllowNavigate=True):
    retOptions = {}
    retOptions['editable'] = Editable
    retOptions['enableAddRow'] = AllowAdd
    retOptions['enableCellNavigation'] = AllowNavigate
    
    return retOptions


    

def addColumn(
              colField, #The field name in the underlying dictionary data
              colID = None,  #Unique Column identifier, defaults to colField if None
              colText = None,  #Text of the column, if blank, we substitute the colField data
              colWidth = None, #Column Width.  If not an integer, then this auto calculates the length
              colCSSClass = None, #should we addd a CSSClass designator?
              resizable = True, #Can the column be resized? (Pass NONE to leave out completley)
              sortable = True, #Can the column be sorted? (Pass NONE to leave out completley)
              minWidth = None,
              maxWidth = None,
              ):
    
    newColumn = {}

    #colField is a required parameter:
    if (colField is None):
        return newColumn

    newColumn['field'] = colField

    #colID
    if (colID) is None:
        newColumn['id'] = colField
    else:
        newColumn['id'] = colID


    if (colText is not None):
        newColumn['name'] = colText
    else:
        newColumn['name'] = colField

    
    if (colWidth is not None):
        #colWidth can accept multiple types of input, see setColumnWidth
        newColumn['width'] = setColumnWidth(colWidth)

    #Pass NONE here to prevent it from being added
    if (resizable is not None):
        newColumn['resizable'] = resizable

    if (sortable is not None):
        newColumn['sortable'] = sortable
        
    #TODO, dynamic assignment of cssClass?
    if (colCSSClass is not None):
        newColumn['cssClass'] = colCSSClass

    if (minWidth is not None):
        newColumn['minWidth'] = minWidth

    if (maxWidth is not None):
        newColumn['maxWidth'] = maxWidth

    return newColumn
