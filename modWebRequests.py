#modWebRequests

import requests
from WebRequests import WebRequests
import json
import os
from modWeb import GetFullDataPath


#Get a value from a dictionary.
#If the key does not exist, return the null value
def getValue(d, v, n=None):
    if (v in d.keys()):
        return (d[v])
    else:
        return (n)

def JSON2Dict(webResponse):
    return json.loads(webResponse)


def CacheObjectName(d):

    
    retVal = "GenericObject"
    #For string objects, return the string name + .webdat
    if (type(d) == type("")):
        retVal = d + ".webdat"

    elif (type(d) == type({})):
        if "CACHENAME" in d.keys():
            retVal = d['CACHENAME'] + ".dynwebdat"
        else:
            retVal = os.path.split(d['URL'])[-1] + ".dynwebdat"
            
    
    

    #Just in case, let's remove any path splitters
    #This may cause trouble in the future,
    #TODO: find a better path sanitization routine

    
        
        
    
    retVal = GetFullDataPath(os.path.split(retVal)[-1])
    return retVal

    

def GetRequest(requestName, forceReload = False, s=None):
    #Set a flag to see if we will use the cache to return this data
    #Default value is to use the Cache
    UseCache = (not forceReload)

    #Also set a flag to see if the results can ever be cached
    PreventCaching = False #Some types cannot be cached

    if (type(requestName) == type({})):
        if "PREVENTCACHING" in requestName.keys():
            PreventCaching = requestName['PREVENTCACHING']

    
    #Can we use the Cache?
    if (UseCache):
        dataFile = str(CacheObjectName(requestName))
        #Get cached data if it exists
        if (os.path.exists(dataFile)):
            dfi = open(dataFile, 'r')
            retData = dfi.read()
            dfi.close()
            

        #Cached object doesn't exist, get it live:
        else:
            UseCache = False
            

    #We were told not to use the cache, Cache was empty, or something went wrong with the cache
    if (not UseCache): #Not Use Cache
        retData = do(requestName, s).content

        #Save our result for later
        if (PreventCaching == False):
            #Cache the data that comes back
            dfi = open(dataFile, 'wb')
            dfi.write(retData)
            dfi.close()

    return retData


def GenerateSession():
    return requests.Session()

def do(requestName, s=None):

    if ( type(requestName) == type([])):
        #Looks like we are being asked for multiple requests
        #We need a session
        s = GenerateSession()
        for r in requestName:
            retVal = do(r, s)
            
        #Return the latest Request
        return retVal.content

    else:
        #Single Request

        if (s==None):
            s = requests.Session()
        
        
        

        
        #Accept reqData as an input
        if (type(requestName) ==  type({})):
            reqData = requestName
        else:
            #Check to see that the request actually exists
            if (requestName not in WebRequests.keys()):
                return None
            reqData = WebRequests[requestName]

        # We must have a valid URL
        url = getValue(reqData, 'URL')
        
        if (url == None):
            return None
    
        
        payLoad = getValue(reqData, 'Attributes')

        authMode = getValue(reqData, 'Auth')

        method = getValue(reqData, 'Method', 'POST')

        reqHeaders = getValue(reqData, 'Headers')

        r=None
        
        if (method == "POST"):

            #Use the "data=payLoad" instead of "params=payLoad" when content-type is x-www-form-urlencoded
            if (reqHeaders):
                if ("content-type") in reqHeaders.keys():
                    if (reqHeaders['content-type'] == "application/x-www-form-urlencoded"):
                        r = r = s.post(url, data=payLoad, auth=authMode, headers=reqHeaders, cookies=s.cookies)
            if (not r):                 
                r = s.post(url, params=payLoad, auth=authMode, headers=reqHeaders)
            
            
            return r
        if (method == "GET"):
            r = s.get(url, params=payLoad, auth=authMode)
            return r
            
        


