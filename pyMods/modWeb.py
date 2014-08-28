
#modWeb.py
#Author: Drew Easley
#Date: August 9, 2014

#This module is responsible for

# isTest() - which will determine if we are deploying this in a test environment
# dthandler - which helps us convert date/time stamps in Python to JSON


import os
import cgi, cgitb
import datetime
from devOpsConfig import globalConfig, modWebConfig
import json
import requests


form = cgi.FieldStorage()

def HttpVar(keyName, defaultValue=None):
    if keyName not in form:
        return defaultValue
    else:
        value = form[keyName]
        if (type(value) == type([])):
            retList = []
            for d in value:
                retList.append(d.value)
            return retList
            
        else:
            #Single Value
            return value.value
        

def GetFullDataPath(relativePath):
    safeFile = os.path.split(relativePath)[-1]
    basepath = os.path.dirname(__file__)
    return (os.path.join(basepath, "data", safeFile))



#Is this _test or Production environment?
def isTest():
    
    isTest = False
    if globalConfig['TEST_DESIGNATOR'] in os.path.dirname(os.path.realpath(__file__)):
        isTest = True
    return isTest


def isWebCall():
    if 'REQUEST_METHOD' in os.environ :
        return True
    else :
        return False

def Sanitize(s):
    return cgi.escape(s)



dthandler = lambda obj: (
	obj.isoformat()
	if isinstance(obj, datetime.datetime)
	or isinstance(obj,datetime.date)
	else None)

def defaultJSONSet():
    retVal = {}
    retVal['UsingTestEnvironment'] = isTest()
    retVal['lastupdate'] = datetime.datetime.now()
    retVal['devOpDashAuthor'] = "Drew E. Easley"
    return retVal

def beginJSON():
    return defaultJSONSet()  #Return a new dictionary

def endJSON(d, prettyPrint=3):
    print("Content-type: application/json\r\n")
    #End headers with a blank line
    print("\r\n")
    print(json.dumps(d, indent=prettyPrint, default=dthandler))

def CGIDebug():
    useDebug = False
    if isTest():
        useDebug = modWebConfig['CGIDEBUG_TEST']
    else:
        useDebug = modWebConfig['CGIDEBUG_PROD']

    if useDebug:
        cgitb.enable()


CGIDebug()


