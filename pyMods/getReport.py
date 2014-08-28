#getReport.py


import modWeb
import modSalesForce
import modDataSummary as r
import modCSV
import os
import modWebRequests
#import modTFS
import urllib


retVal = modWeb.beginJSON()

#Some basics just to make sure something gets written





RequireLive = False
reportData = None

if modWeb.isWebCall():
    SummaryMode = modWeb.HttpVar('SUMMARYMODE', 0)
    SummaryCol1 = modWeb.HttpVar('ATTRIBUTE1')
    SummaryCol2 = modWeb.HttpVar('ATTRIBUTE2')
    ReportID = modWeb.HttpVar('REPORTID')
    RequireLive = modWeb.HttpVar('REQUIRELIVE', False)
    ReportSource = modWeb.HttpVar('SOURCE', "NODATA")

    #Decode the URL
    ReportID = urllib.unquote(ReportID).decode('utf8')
    
else:
    
    RequireLive = False
    SummaryMode = 0

    #Sales Force Report (All Open or Dev Escalation)
    ReportSource = 'SALESFORCE'
    ReportID = '00O30000008Rd2B' #'00O30000008SLvB' 
    # SummaryCol1 = 'Case Owner'
    # SummaryCol2 = 'Status'

    #CSV - TFS Open Bugs
    #ReportSource = 'CSV'
    #ReportID = 'c:\\devOps\\SFTFSIntegration\\AllOpenBugs.csv'
    #SummaryCol1 = 'State'
    #SummaryCol2 = 'Severity'

    #TFS Pull list of Querues
    #ReportSource = 'WEB'
    #ReportID = 'TFS_QUERIES'

    #TFS Direct Query by ID
    #ReportSource = 'TFS'
    #ReportID = 'doAllOpenBugs'
    #SummaryMode = 0
    #SummaryCol1 = 'System.State'
    #SummaryCol2 = 'System.AssignedTo'

    

retVal['REPORTID'] = ReportID
retVal['CACHED'] = not RequireLive


#Get Data for SalesForce
if (ReportSource.upper() == 'SALESFORCE'):
    if (ReportID is None):
        reportData = {'ERROR' : 'ReportID parameter was not specified'}
        
    #elif (RequireLive):
    sfDataSource = modSalesForce.GetReport(ReportID, UseLive=RequireLive)
    reportData = sfDataSource.asDict()
    


#Get Data for CSV Files
if (ReportSource.upper() == 'CSV'):
    if (ReportID is None):
        reportData = {'ERROR' : 'ReportID parameter was not specified'}
    else:
        #Force the CSV file location to be in the data folder
        #This should help protect our security by preventing access to non-acceptable files
        fileName = os.path.split(ReportID)[-1] #Get the filename only
        reportData = modCSV.ReadFile(os.path.join("data", fileName))


if (ReportSource.upper() == 'WEB'):
    reportData = modWebRequests.JSON2Dict(modWebRequests.GetRequest(ReportID))


if (ReportSource.upper() == 'TFS'):
    ds = modTFS.GetReport("[O]racle")
    ReportSource = ds.outAsJSON()

if (ReportSource.upper() == 'NODATA'):
    reportData = {'ERROR' : 'No cgi parameter SOURCE was specified.'}


    

#Summary Switches


if (SummaryMode == 0):
    if (reportData is not None):
        retVal['REPORT'] = reportData

if (SummaryMode == 1):
    retVal ['SUMMARYOF'] = SummaryCol1
    retVal ['SUMMARY1D' ] = r.Summarize(reportData, SummaryCol1)
if (SummaryMode == 2):
    retVal ['SUMMARYOF'] = SummaryCol1 + " and " + SummaryCol2
    retVal['SUMMARY2D'] = r.Summarize2D(reportData, SummaryCol1, SummaryCol2)



modWeb.endJSON(retVal)
