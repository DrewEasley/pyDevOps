#modSalesForce
from WebRequests import WebRequests
import modWebRequests
import modCSV
import os
from modWeb import GetFullDataPath




#x = GetReportLive("00O30000008Rd2B")
def GetReportLive(ReportID):
    SfReportRequest = WebRequests['Salesforce_Report']
    SfReportRequest
    SfReportRequest['URL'] = SfReportRequest['URL'].format(ReportID)
    SfReportRequest['CACHENAME'] = SfReportRequest['CACHENAME'].format(ReportID)
    webQueue = ['Salesforce_Login', SfReportRequest]

    data = modWebRequests.do(webQueue)
    
    pyData = modCSV.ReadCSVStream(data)
    modCSV.WriteCSV(pyData, os.path.join("data", ReportID + ".csv"))
    return pyData



#x = GetReportCached("00O30000008Rd2B")
def GetReportCached(ReportID):
    dataFile = GetFullDataPath(ReportID + ".csv")
    #dataFile = os.path.join("data", ReportID + ".csv")
    if (os.path.exists(dataFile)):
        pyData = modCSV.ReadFile(dataFile)
    else:
        #Cached copy doesn't exist, we need to fetch it live.
        pyData = GetReportLive(ReportID)
    return pyData




#print x
