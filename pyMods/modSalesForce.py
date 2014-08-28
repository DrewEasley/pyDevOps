#modSalesForce
from WebRequests import WebRequests
import deepDataDictionary

import modWebRequests
import modCSV





def GetReport(ReportID, IDColumn, UseLive = False):
    SfReportRequest = WebRequests['Salesforce_Report']
    SfReportRequest['URL'] = SfReportRequest['URL'].format(ReportID)
    webQueue = ['Salesforce_Login', SfReportRequest]
    #data = GetObject(webQueue, forceReload= UseLive)
    data = modWebRequests.do(webQueue)
    pyData = modCSV.ReadCSVStream(data)
    ds = deepDataDictionary.newFromPydict("SalesForce", ReportID, pyData)
    ds.setIDColumn(IDColumn)
    return ds
    #return pyData


#REPORT_ID = "00O30000008Rd2B"

#dx = deepDataDictionary.newFromPydict("SalesForce", REPORT_ID, GetReport(REPORT_ID))
