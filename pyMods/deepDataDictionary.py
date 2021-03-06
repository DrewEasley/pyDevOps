#deepDataDictionary


from devOpsConfig import globalConfig
import hmac
import modDataCache
import json
import cPickle as ca
import modDataSummary
import datetime
import os






def loadPickle(cacheObjectName):
    if (os.path.exists(cacheObjectName)):
        d = ca.load(open(cacheObjectName, 'rb'))
        d.cacheAge = (datetime.datetime.now() - d.cacheTime)
        return d
    else:
        return None

def savePickle(cacheObjectName, obj):
    obj.cacheTime = datetime.datetime.now()
    ca.dump(obj, open(cacheObjectName, 'wb'))

class DataSource:

    myRequest = {}
    myColumns = {}
    myMetaData = {}
    cacheTime = None
    cacheAge = None
    myRows = []

    mySource = ""
    
    useMod = None
    useCache = False
    idColumn = 0

    def isStale(self, seconds = 0, minutes = 0, hours = 0, days = 0):
        dd = datetime.timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
        return (dd  < self.cacheAge)

    def Summarize1(self, columnName):
        d = self.asDict()
        return modDataSummary.Summarize(d, columnName)

    def Summarize2(self, column1Name, column2Name):
        d = self.asDict()
        return modDataSummary.Summarize2D(d, column1Name, column2Name)


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
                if len(r) > 0:
                    retItem['id'] = r[self.idColumn]
            retD.append(retItem)
        retD2 = {}
        retD2['REPORT'] = retD
        retD2['MetaData'] = self.myMetaData
        
        return retD2
    
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
        #rint self.myRequest
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
    #    rint cHeaders
    #    for r in self.myRows:
    #        rint str(r)[1:-1]
    #    #for r in self.myRows:
    #        #rint r

    def outAsJSON(self, PrettyPrint=2):
        
        
        return json.dumps(self.asDict(), indent=PrettyPrint)
        
        
        

    

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
        #rint MyRecord
        d.addData([MyRecord])
    return d

    
        
    
