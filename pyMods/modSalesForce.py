#modSalesForce
from WebRequests import WebRequests
import deepDataDictionary

import modWebRequests
import modCSV





def GetReport(ReportID, UseLive = False):
    SfReportRequest = WebRequests['Salesforce_Report']
    SfReportRequest['URL'] = SfReportRequest['URL'].format(ReportID)
    webQueue = ['Salesforce_Login', SfReportRequest]
    #data = GetObject(webQueue, forceReload= UseLive)
    data = modWebRequests.do(webQueue)
    pyData = modCSV.ReadCSVStream(data)
    return pyData


REPORT_ID = "00O30000008Rd2B"

dx = deepDataDictionary.newFromPydict("SalesForce", REPORT_ID, GetReport(REPORT_ID))
