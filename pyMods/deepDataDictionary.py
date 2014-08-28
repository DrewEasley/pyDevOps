#deepDataDictionary


from devOpsConfig import globalConfig
import hmac
import modDataCache
import json
import cPickle as ca
import modDataSummary




def loadPickle(cacheObjectName):
    d = ca.load(open(cacheObjectName, 'rb'))


class DataSource:

    myRequest = {}
    myColumns = {}
    myMetaData = {}
    
    myRows = []

    mySource = ""
    
    useMod = None
    useCache = False
    idColumn = 0

    def Summarize1(self, columnName):
        d = self.asDict()
        return modDataSummary.Summarize(d, columnName)

    def Summarize2(self, column1Name, column2Name):
        d = self.asDict()
        return modDataSummary.Summarize2D(d, column1Name, column2Name)

    def savePickle(self, cacheObjectName):
        ca.dump(self, open(fName, 'wb'))

    def numRows(self):
        return len(self.myRows)

    def myColumnNames(self):
        retVal = []
        for x in self.myColumns:
            retVal.append(self.myColumns[x]['name'])
        return retVal

    def setIDColumn(self, name):
        for i in self.myColumns:
            if name.upper() == self.myColumns[i]['name'].upper():
                self.idColumn = i
        

    #Add a row to data source
    def addData(self, rowData):
        self.myRows = self.myRows + rowData
            

    def addMetaData(self, d):
        self.myMetaData = d


    def asDict(self):
        retD = []
        for r in self.myRows:
            retItem = {}
            for c in self.myColumns:
                cName = self.myColumns[c]['name']
                cValue = r[c]
                retItem[cName] = cValue
            if ('id' not in retD):
                retItem['id'] = r[self.idColumn]
            retD.append(retItem)
        return retD
    
    def addColumn(self, name, label=None, width=None, sorttype=None, summaryType = None, sortable=True, groupable = False):
        idx = len(self.myColumns)
        self.myColumns[idx] = {
            'name': name,
            'label': label,
            'width': width,
            'sorttype': sorttype,
            'searchoptions' : None,
            'summaryType' : summaryType,
            'sortable': sortable,
            'groupable': groupable,
            }

    
    def setMyRequest(self, d, sou):
        self.myRequest = d
        self.mySource = sou
        #print self.myRequest
        return self

    def myName(self):
        caller = ""

        myR = str(self.myRequest) #String representation of our definition

        nameTemplate = "{0}.{1}"
        secKey = globalConfig['SECURITYKEY']
        h = hmac.new(secKey)
        h.update(myR)
        objhash = h.hexdigest()

        return nameTemplate.format(self.mySource, objhash)

    #def outAsCSV(self):
    #    cHeaders = ""
    #    for c in self.myColumns:
    #        cName = self.myColumns[c]['name']
    #        if (len(cHeaders) > 0):
    #            cHeaders = cHeaders + ","
    #        cHeaders = cHeaders + cName
    #    print cHeaders
    #    for r in self.myRows:
    #        print str(r)[1:-1]
    #    #for r in self.myRows:
    #        #print r

    def outAsJSON(self, PrettyPrint=2):
        retD = self.asDict()
            
        return json.dumps(retD, indent=PrettyPrint)
        
        
        


def newFromPydict (mySource, RequestData, dictionarydata, RecordWithAllColumns = 0):
    d = DataSource()
    d.setMyRequest(RequestData, mySource)
    

    #We received a set of Dictionary rows (hopefully)

    Columns = dictionarydata[RecordWithAllColumns].keys()
    #Add all unique columns to our database
    for c in Columns:
        d.addColumn(c)


    for r in dictionarydata:
        MyRecord = []
        for c in d.myColumnNames():
            rValue = r[c]
            MyRecord.append(rValue)
        #print MyRecord
        d.addData([MyRecord])
    return d

    
        
    
