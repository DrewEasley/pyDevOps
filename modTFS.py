#modTFS

import modWebRequests
import json
from StringIO import StringIO
from WebRequests import WebRequests
import xml.etree.ElementTree as etree





def GetQueries(TFS_QUERIES_NAME = "TFS_QUERIES", forceReload = False):
    
    
    qData = modWebRequests.GetRequest(TFS_QUERIES_NAME, forceReload)
    return (json.load(StringIO(qData)))


def FindQuery(iden, col, RequireLiveData= False):

    
    QRYData = GetQueries(forceReload = RequireLiveData)
    QryTypes = ['publicQueries', 'privateQueries'] # Skip Assigned to Me and UnSaved Work Items

    for qType in QryTypes:
        for qry in QRYData[qType]:
            val = qry[col].encode('ascii', errors='ignore')
            if (val.upper() == iden.upper()):
                return qry

        
    return None
    




def FindQueryByName(name, RequireLiveData = False):
    return FindQuery(name, "name", RequireLiveData=RequireLiveData)

def FindQueryById(name, RequireLiveData = False):
    return FindQuery(name, "id", RequireLiveData=RequireLiveData)    


def QueryMethod(q):
    return q['query']

def QueryID(q):
    return q['id']



def GetAFT(data):
    #We need to get the <input name="__RequestVerificationToken"> value from the first TFS Request
    root = etree.fromstring(data)
    body = root.find("{http://www.w3.org/1999/xhtml}body")
    token_e = body.find("{http://www.w3.org/1999/xhtml}input/[@name='__RequestVerificationToken']")
    return token_e.attrib['value']
    
    
def GetUpdQueryURL(data):
    findStr = "window.location.replace("
    i = data.find(findStr)    #Find window.location.replace(
    j = data.find("\");", i)  #Find the ending ");
    return data[i + len(findStr) +1 :j]
    


def PayloadDictionary(rawd):
    if (not type(rawd) == type({})):
        return {'ERROR': 'TFS Raw Data was not a Dictionary.'}

    if ("queryRan" not in rawd.keys()):
        return {'ERROR': 'Does not appear to be a TFS Query Execution.'}

    if (rawd['queryRan'] == False):
        return {'ERROR': 'TFS Query did not run.'}

    #Get some basic data about the query
    sortColumns = rawd['sortColumns']
    pageColumns = rawd['pageColumns']
    editInfo = rawd['editInfo']
    targetIDs = rawd['targetIds']
    wiql = rawd['wiql']
    payload = rawd['payload']
    columns = rawd['columns']
    queryRan = rawd['queryRan']

    retVal = {}

    #True/False, did the Query Run?
    retVal['queryRan'] = queryRan

    #List Sort Order in a simple list of columns
    sortOrder = []
    for sortColumn in sortColumns:
        sortOrder.append(sortColumn['name'])
    retVal['SortedBy'] = sortOrder


    #Return the columns in this query
    retVal['DataColumns'] = pageColumns

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
    

    
    
    return retVal

def ExecuteQuery(query, useLive = False):

    if (query is None):
        return None

    query_template = []
    qry_id = QueryID(query)
    qry_wiql = QueryMethod(query)



    #We need to make two requests, we need to make them under the same web session.
    tfs_session = modWebRequests.GenerateSession()
    

    #Step 1: Get the correct path to the Query (what the user would see in TFS)
    req1 = WebRequests['TFS_QUERYROOT']
    TFS_ROOT = req1['ROOT']
    TFS_PROJ = req1['PROJ']

    template_url = req1['URL']
    req1['URL'] = template_url.format(TFS_ROOT, TFS_PROJ, "_workItems/resultsById/" +qry_id)
    req1['PREVENTCACHING'] = True
    req1_data = modWebRequests.GetRequest(req1, forceReload=useLive, s=tfs_session)
    req1_newUrl = GetUpdQueryURL(req1_data)
    #End Step 1



    #Step 2, make a request, and get the __AntiForgeryToken from the TFS Results
    #This is a simple re-direct, so we keep everything else the same
    req1['URL'] = template_url.format(TFS_ROOT, req1_newUrl, "")       
    req2_data = modWebRequests.GetRequest(req1, forceReload=useLive, s=tfs_session)
    AFToken = GetAFT(req2_data)


    #Step 3, execute the request for JSON data, passing the AFT as __RequestVerificationToken
    req3 = WebRequests['TFS_QUERY']
    req3['URL'] = req3['URL'].format(TFS_ROOT, TFS_PROJ, '_api/_wit/query?__v=1')
    req3['Attributes']['wiql'] = QueryMethod(query)
    req3['Attributes']['__RequestVerificationToken'] = AFToken

    queryName = query['name']
    req3['CACHENAME'] = req3['CACHENAME'].format(queryName)
    

    
    
    req3_data = modWebRequests.GetRequest(req3, forceReload=useLive, s=tfs_session)
    return modWebRequests.JSON2Dict(req3_data)
    
