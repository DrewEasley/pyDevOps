#modSalesForce
from WebRequests import WebRequests
import modWebRequests
import modCSV
import os
from modWeb import GetFullDataPath
import modDataCache
import copy


def GetObject(r, forceReload = False, forceCache=False, webSession = None, withSave=True):
    MyName = "SALESFORCE"
    r_ForCache = copy.deepcopy(r)

    r_ForCache = r_ForCache[:1]
    
    if (not forceReload):
        res = modDataCache.LoadFromCache(MyName,r_ForCache)
        
    else:
        #Force the reload, set Result to None
        res = None

    if ((res is None) and not forceCache):
        
        #Object was not in Cache, we need to load remotely (and we are allowed to)
        res = modWebRequests.do(r, s=webSession)
        if (withSave):
            modDataCache.SaveToCache(MyName, r_ForCache, res)

    return res

def GetReport(ReportID, UseLive = False):
    SfReportRequest = WebRequests['Salesforce_Report']
    SfReportRequest['URL'] = SfReportRequest['URL'].format(ReportID)
    webQueue = ['Salesforce_Login', SfReportRequest]
    data = GetObject(webQueue, forceReload= UseLive)
    pyData = modCSV.ReadCSVStream(data)
    return pyData



