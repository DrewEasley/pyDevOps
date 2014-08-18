#modWebRequests

import requests
from WebRequests import WebRequests
import json
import os
from modWeb import GetFullDataPath
import urlparse


#Get a value from a dictionary.
#If the key does not exist, return the null value
def getValue(d, v, n=None):
    if (v in d.keys()):
        return (d[v])
    else:
        return (n)

def JSON2Dict(webResponse):
    return json.loads(webResponse)



#def CacheObjectName(d):
#CacheObjectName is removed, and replaced by the entire modDataCache library

    

def GetRequest(requestName, s=None):
    retData = do(requestName, s).content
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
            
        


def JSRedirectURL(URLRoot, data):
    findStr = "window.location.replace("
    i = data.find(findStr)   #Find window.location.replace(
    j = data.find("\");", i) #Find the ending ");
    subUrl = data[i + len(findStr) + 1: j]
    return urlparse.urljoin(URLRoot, subUrl)
    

