#modSalesForce
from WebRequests import WebRequests
import deepDataDictionary

import modWebRequests
import modCSV
import datetime
from devOpsConfig import modSFConfig


MAX_CACHE_MINUTES = modSFConfig['CACHE_EXPIRE_MINUTES']

def getPiclName(ReportID):
    return "data//sf_{0}.picl".format(ReportID)

def GetCachedReport(ReportID, IDColumn):
    ds = deepDataDictionary.loadPickle(getPiclName(ReportID))
    
 
    if (ds is not None):
        if ds.isStale(minutes = 15):
            #Record is Stale. Fetch Live
            ds = None
    
    if (ds is None):
        ds = GetReport(ReportID, IDColumn)


    return ds


def GetReport(ReportID, IDColumn):
    SfReportRequest = WebRequests['Salesforce_Report']
    SfReportRequest['URL'] = SfReportRequest['URL'].format(ReportID)
    webQueue = ['Salesforce_Login', SfReportRequest]
    #data = GetObject(webQueue, forceReload= UseLive)
    data = modWebRequests.do(webQueue)
    pyData = modCSV.ReadCSVStream(data)
    ds = deepDataDictionary.newFromPydict("SalesForce", ReportID, pyData)
    #ds.setIDColumn(IDColumn)
    #deepDataDictionary.savePickle(getPiclName(ReportID), ds)
    return ds
    #return pyData


#REPORT_ID = "00O30000008Rd2B"

#dx = deepDataDictionary.newFromPydict("SalesForce", REPORT_ID, GetReport(REPORT_ID))


GetCachedReport('00O30000008Rd2B', 'Case Number')
