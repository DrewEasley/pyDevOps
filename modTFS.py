#modTFS

import modWebRequests
import json
from StringIO import StringIO
from WebRequests import WebRequests
import xml.etree.ElementTree as etree
import modReporting
from urlparse import urljoin




        
    



#Unit Tested by : modTFSUnitTests.test_API_Endpoints looks for
#the presence of AFT_ROOT and QUERY_LIST as required in this array
TFS_API_ENDPOINTS = {
        'AFT_ROOT': '_workItems/resultsById/{0}',
        'QUERY_LIST': '_api/_wit/queries',
        'QUERY_FETCH': '_api/_wit/query?__v=1'
    }


#Unit Tested by : test_loadTFSTemplate
def LoadTFSTemplate(templateName):
    template = WebRequests[templateName]
    return template

#Unit Tested by : test_getTFSRoot
def getTFSRoot(templateName = 'TFS2010_TEMPLATE'):
    t = LoadTFSTemplate(templateName)
    return t['TFSHOME']

#Unit Tested by : test_PreprareTFSRequest
def PrepareTFSRequest(endpoint, param, templateName = 'TFS2010_TEMPLATE', cacheName = None, requirePost = False):
    t = LoadTFSTemplate(templateName)
    
    tfshome = getTFSRoot(templateName)
    tfsproj = t['TFSPROJ']

    
    projurl = urljoin(tfshome, tfsproj)

    
    
    endpoint = TFS_API_ENDPOINTS[endpoint]
    endpoint = endpoint.format(param)
    
    url = urljoin(projurl, endpoint)
    t['URL'] = url

    if (cacheName is not None):
        t['CACHEAS'] = cacheName

    if (requirePost):
        t['Method'] = 'POST'
    
    #Remove extra data we don't need right now
    
    #t.pop('PROJ')
    #t.pop('HOME')
    
    return t

#Unit Tested by : test_AddRequestAttribute
def AddRequestAttribute(t, attName, attValue):
    if ('Attributes' not in t.keys()):
        t['Attributes'] = {}

    t['Attributes'][attName] = attValue
    return (t)

#Unit Tested by : test_GetQueries
def GetQueries(templateName='TFS2010_TEMPLATE', forceReload = False):
    t = PrepareTFSRequest('QUERY_LIST', None, templateName, cacheName = 'TFSQueryList')
    t = AddRequestAttribute(t, 'includeQueryTexts', 'true') #Request Query Text
    qData = modWebRequests.GetRequest(t, forceReload)
    return (json.load(StringIO(qData)))


#Unit Tested by : test_FindQuery
def FindQuery(iden, col, RequireLiveData= True):

    QRYData = GetQueries(forceReload = RequireLiveData)
    QryTypes = ['publicQueries', 'privateQueries'] # Skip Assigned to Me and UnSaved Work Items
    for qType in QryTypes:
        for qry in QRYData[qType]:
            val = qry[col].encode('ascii', errors='ignore')
            if (val.upper() == iden.upper()):
                return qry

        
    return None

#Unit Tested by : test_FindQuery
def FindQueryByName(name, RequireLiveData = False):
    return FindQuery(name, "name", RequireLiveData=RequireLiveData)

#Unit Tested by : test_FindQuery
def FindQueryById(name, RequireLiveData = False):
    return FindQuery(name, "id", RequireLiveData=RequireLiveData)    

#Unit Tested by : test_FindQuery
def QueryMethod(q):
    return q['query']

#Unit Tested by : test_FindQuery
def QueryID(q):
    return q['id']


#Unit Tested by: test_GetAFT
def GetAFT(data):
    #We need to get the <input name="__RequestVerificationToken"> value from the first TFS Request
    root = etree.fromstring(data)
    body = root.find("{http://www.w3.org/1999/xhtml}body")
    token_e = body.find("{http://www.w3.org/1999/xhtml}input/[@name='__RequestVerificationToken']")
    return token_e.attrib['value']
    

  

#Unit Tested by: test_ConvertFromTFSDate
def ConvertFromTFSDate(d):
    #Input: /Date(1407999345210)/
    d=d.replace("/Date(","").replace(")/","")
    d=float(d)
    #Output: 1407999345210.0
    return d
    

#Unit Tested by: test_CleanupTFSPayload
def CleanupTFSPayload(payload, parentLookup):
    retData = []


    #Setup our column Dictionary
    colDict = {}

    UniqueIDCol = -1
    i = 0
    for column in payload['columns']:
        if (column == 'System.Id'):
            UniqueIDCol = i
        colDict[i] = column
        i = i+1

    
    #Load Rows

    
    for row in payload['rows']:
        retItem = {}
        
        for colNum in colDict.keys():
            colName = colDict[colNum]
            val = row[colNum]
            if (
                (type(val) == type("")) or
                (type(val) == type(u""))):
                    if "/Date(" in val:
                        val = ConvertFromTFSDate(val)
                
            retItem[colName] = val
        #The 'id' field must be populated with a unique ID
        retItem['id']= row[UniqueIDCol]
        if (parentLookup is not None):
            if (retItem['id'] in parentLookup.keys()):
                if (parentLookup[retItem['id']] == None):
                    retItem['parent'] = None
                elif (parentLookup[retItem['id']] == 0):
                    retItem['parent'] = None
                else:                  
                    retItem['parent'] = parentLookup[retItem['id']]
        
        retData.append(retItem)
    
    return retData

    


#Unit Tested by: test_PayloadDict
def PayloadDictionary(rawd, columnData="verbose", IncludeTargetIds=False, IncludePayload=True):
    retVal = {}

    
    if (not type(rawd) == type({})):
        return {'ERROR': 'TFS Raw Data was not a Dictionary.'}

    if ("queryRan" not in rawd.keys()):
        return {'ERROR': 'Does not appear to be a TFS Query Execution.'}

    if (rawd['queryRan'] == False):
        return {'ERROR': 'TFS Query did not run.'}

    #Get some basic data about the query
    sortColumns = rawd['sortColumns']


    #VerboseColumnData = rawd['columns']
    VerboseColumnData = []
    for col in rawd['columns']:
        
        cn = col['name']
        ci = col['fieldId']
        cT = col['text']
        cW = col['width']
        cS = col['canSortBy']      
        cd = modReporting.addColumn(cn, colID=ci, colText=cT, colWidth= cW, sortable=cS)
        VerboseColumnData.append(cd)
    
        
    SimpleColumnData = rawd['pageColumns']
    
    
    #editInfo = rawd['editInfo']

    
    targetIDs = rawd['targetIds']
    retVal['totalItems'] = len(targetIDs)
    retVal['thisPage'] = len(rawd['payload'])
    
    payload = rawd['payload']


    parentLookup = {}

    i = 0
    
    
    if ('sourceIds' in rawd.keys()):
        sourceIds = rawd['sourceIds']
        
        for t in targetIDs:
            currentTarget = targetIDs[i]
            
            parentTarget = sourceIds[i]
            if (int(parentTarget) == 0):
                parent = None
            else:
                parent = i #parentTarget
            parentLookup[currentTarget] = parent
            i = i+1
            
    
    wiql = rawd['wiql']
    
    
    queryRan = rawd['queryRan']



    
    retVal['LOG'] = []

    #True/False, did the Query Run?
    retVal['queryRan'] = queryRan


    #List Sort Order in a simple list of columns
    sortOrder = []
    for sortColumn in sortColumns:
        sortOrder.append(sortColumn['name'])
    retVal['SortedBy'] = sortOrder


    #Return the columns in this query
    
    if (columnData.upper() == "VERBOSE"):
        retVal['columns'] = VerboseColumnData
        
        retVal['LOG'].append ("Column Data: Verbose")
    
    elif (columnData.upper() == "NONE"):
        #Specifc request to not include columnData
        retVal['LOG'].append ("Column Data:  None")
    else:
        #Put simple column data in for all others
        retVal['columns'] = SimpleColumnData
        retVal['LOG'].append ("Column Data: Simple")

    #editInfo <-- Skip.  No need to return this to client, as no TFS access is available.
    #Perhaps one day we can expose the query definition this way?
    #Example editInfo returned...
    #print json.dumps(retVal['REPORT']['editInfo'], indent=2)
    ##{
    ##  "sourceFilter": {
    ##    "clauses": [
    ##      {
    ##        "operator": "=", 
    ##        "index": 1, 
    ##        "fieldName": "Team Project", 
    ##        "value": "PROJ1", 
    ##        "logicalOperator": ""
    ##      }, 
    ##      {
    ##        "operator": "=", 
    ##        "index": 2, 
    ##        "fieldName": "Work Item Type", 
    ##        "value": "User Story", 
    ##        "logicalOperator": "And"
    ##      }, 
    ##      {
    ##        "operator": "<>", 
    ##        "index": 3, 
    ##        "fieldName": "State", 
    ##        "value": "Done", 
    ##        "logicalOperator": "And"
    ##      }, 
    ##      {
    ##        "operator": "<>", 
    ##        "index": 4, 
    ##        "fieldName": "State", 
    ##        "value": "Removed", 
    ##        "logicalOperator": "And"
    ##      }
    ##    ], 
    ##    "maxGroupLevel": 0, 
    ##    "groups": []
    ##  }, 
    ##  "mode": 1
    ##}

    #wiql <--  Skip this as well, no need to return it
    #print retVal['REPORT']['wiql']
    ##select [System.Id], [System.State], [Microsoft.VSTS.Common.Severity],
    ##[System.Title], [System.IterationPath], [System.AssignedTo],
    ##[System.ChangedBy], [System.ChangedDate], [Microsoft.VSTS.Common.StackRank],
    ##[System.CreatedBy] from WorkItems where
    ##[System.TeamProject] = 'PROJ1' and [System.WorkItemType] = 'User Story' and
    ##[System.State] <> 'Done' and [System.State] <> 'Removed' order by
    ##[Microsoft.VSTS.Common.Severity]

    

    #Straight list of IDs included in the report

    if (IncludeTargetIds):
        retVal['targetIds'] = targetIDs


    if (IncludePayload):
        retVal['payload'] = CleanupTFSPayload(payload, parentLookup)
    
    return retVal


#NOT UNIT TESTED! This uses live data, and would be an integration test

def ExecuteQuery_Step1(qry_id, tfsSession, useLive = False):
    #Step 1: Get the correct path to the Query (what the user would see in TFS)
    Request1 = PrepareTFSRequest('AFT_ROOT', qry_id)
    Request1['PREVENTCACHING'] = True
    TFS_ROOT = Request1['TFSHOME']
    req1_data = modWebRequests.GetRequest(Request1, forceReload=useLive, s=tfsSession)

    #Our response contains a window.location.replace(URL) command in javascript
    #this modWebRequests function will figure out what URL we need to go to

    
    req1_newUrl = modWebRequests.JSRedirectURL(TFS_ROOT, req1_data)
    return req1_newUrl


def ExecuteQuery_Step2(url, tfsSession, useLive = False):
    Request2 = PrepareTFSRequest('AFT_ROOT', None) #It does not matter what endpoint you use, we rewrite the URL below
    Request2['URL'] = url
    req2_data = modWebRequests.GetRequest(Request2, forceReload=useLive, s=tfsSession)
    AFToken = GetAFT(req2_data)
    return AFToken
    
    

def ExecuteQuery(query, useLive = False, includePayload = True, includeColumnData="verbose", includeTargetIds = False):

    
    if (query is None):
        return None

    query_template = []
    qry_id = QueryID(query)
    qry_wiql = QueryMethod(query)



    #We need to make two requests, we need to make them under the same web session.
    tfs_session = modWebRequests.GenerateSession()
    
    #The user has passed us a query to execute.  TFS will use Javascript to redirect us to the actual
    #landing page.  Let's get that redirect URL ourselves since python requests cannot follow javascript redirects (yet?)
    js_returnURL = ExecuteQuery_Step1(qry_id, tfs_session, useLive)
    
    #Step 2, make a request to the new URL, and get the __AntiForgeryToken from the TFS Results
    AFToken = ExecuteQuery_Step2(js_returnURL, tfs_session, useLive)
    


    #Step 3, execute the request for JSON data, passing the AFT as __RequestVerificationToken
    queryName = query['name']   
    Request3CacheName = "TFS_QUERY_{0}.tfsdat".format(queryName)
    Request3 = PrepareTFSRequest('QUERY_FETCH', None, requirePost = True, cacheName = Request3CacheName)
    #req3['URL'] = req3['URL'].format(TFS_PROJ, '')
    Request3['Headers'] = {'content-type': 'application/x-www-form-urlencoded'}

    if ('Attributes' not in Request3.keys()):
        Request3['Attributes'] = {}
    
    Request3['Attributes']['wiql'] = QueryMethod(query)
    Request3['Attributes']['runQuery'] = True
    Request3['Attributes']['__RequestVerificationToken'] = AFToken
 
    
    
    
    req3_data = modWebRequests.GetRequest(Request3, forceReload=useLive, s=tfs_session)

    rawDict = modWebRequests.JSON2Dict(req3_data)
    
    return PayloadDictionary(rawDict, columnData=includeColumnData, IncludeTargetIds=includeTargetIds, IncludePayload=includePayload)
    

