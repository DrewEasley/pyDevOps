# -*- coding: cp1252 -*-
#modTFSUnitTests.py

import unittest
import modTFS
import random

TFS_TEMPLATE_NAME = 'TFS2010_TEMPLATE'

def GenerateSampleData(numRows = 50):
    retVal = {}

    payload = {}
    payload['columns']= [u'System.State', u'Microsoft.VSTS.Common.Severity', u'System.Id', u'System.Title'] 
    payload['rows'] = []
    #Test is written so System.ID is always column #2

    
    retVal['queryRan'] = True
    
    retVal['pageColumns'] = payload['columns']

    retVal['targetIds'] = []
    for i in range(0,numRows):
        retVal['targetIds'].append(i)
    
    #Sample WIQL to go with our sample DATA
    retVal['wiql'] = "select [System.State], [Microsoft.VSTS.Common.Severity], [System.Id], [System.Title] from WorkItems where [System.TeamProject] = 'PROJ1' order by [System.State]"
    
    

    retVal['columns'] = []
    for c in payload['columns']:
        colItem = {}
        colItem['name'] = c #Column Name
        colItem['fieldId'] = random.randint(-4,50) #Random Field ID, some are negative in TFS. 
        colItem['text'] = c  #Column Text
        colItem['width'] = random.randint(5,25)  #Random width integer
        colItem['canSortBy'] = bool(round(random.random())) # Random True/False
        retVal['columns'].append(colItem)


    #Fake some sortColumns as the first two columns of our data
    retVal['sortColumns'] = retVal['columns'][0:2]

    
    for r in range(0,numRows):
        row = []
        for c in payload['columns']:
            d = random.randint(0,100)
            row.append(d)
        payload['rows'].append(row)
    

    retVal['payload'] = {}
    retVal['payload']['columns'] = payload['columns']
    retVal['payload']['rows'] = payload['rows']
    return retVal


class TestmodTFS(unittest.TestCase):
    def setUp(self):
        pass

    def test_API_Endpoints(self):
        required_endpoints_found = True

        requiredEndpoints = []
        requiredEndpoints.append('AFT_ROOT')
        requiredEndpoints.append('QUERY_LIST')
        requiredEndpoints.append('QUERY_FETCH') #'_api/_wit/query?__v=1

        definedEndpoints = modTFS.TFS_API_ENDPOINTS
        for ep in requiredEndpoints:
            try:
                self.assertTrue(ep in definedEndpoints)
            except:
                required_endpoints_found = False


        self.assertTrue(required_endpoints_found)

    #Test to make sure TFS2010_TEMPLATE exists in WebRequests
    #This should probably be pushed into the WebRequests unit test
    #Also tests modTFS.LoadTFSTemplate(templateName)
    def test_loadTFSTemplate(self):
        
        t = modTFS.LoadTFSTemplate(TFS_TEMPLATE_NAME)
        required_keys = []
        errorText = "WebRequests[{0}][{1}] is not present. Please see documentation."

        required_keys.append('TFSPROJ')
        required_keys.append('TFSHOME')
        required_keys.append('Method')
        required_keys.append('Auth')

        for rKey in required_keys:
            err = errorText.format(TFS_TEMPLATE_NAME, rKey)
            self.assertTrue(rKey in t, err)

        self.assertEqual(t['Method'].upper(), 'GET', TFS_TEMPLATE_NAME + '[Method] must be GET not ' + str(t['Method']))

    def test_getTFSRoot(self):
        t = modTFS.getTFSRoot(TFS_TEMPLATE_NAME)
        self.assertTrue("http" in t, str(t) + " does not look like a valid root URL to TFS")

    
    def test_PrepareTFSRequest(self):
        endPointsToTest = []
        #endPointsToTest.append('AFT_ROOT')
        endPointsToTest.append('QUERY_ROOT')
        rData = str(random.randint(100,255))
        rDatb = str(random.randint(100,255))

        
        qry_list = modTFS.PrepareTFSRequest('QUERY_LIST', rData, TFS_TEMPLATE_NAME)
        

        
        desiredURL = '/_api/_wit/queries'

        #URL should end with /_api/_wit/queries
        self.assertTrue(qry_list['URL'].endswith(desiredURL))


        rDatc = str(random.randint(100,255))
        rDatd = str(random.randint(100,255))
        aft_data = modTFS.PrepareTFSRequest('AFT_ROOT', rDatc, TFS_TEMPLATE_NAME)
        desiredURL = '_workItems/resultsById/' + rDatc
        
        self.assertTrue(aft_data['URL'].endswith(desiredURL))
        

        

    def test_AddRequestAttribute(self):
        qry_list = modTFS.PrepareTFSRequest('QUERY_LIST', None, TFS_TEMPLATE_NAME)
        t = modTFS.AddRequestAttribute(qry_list, 'UNITTEST', 'UTVALUE')
        self.assertEquals(t['Attributes']['UNITTEST'], 'UTVALUE')

    def test_GetQueries(self):
        qr = modTFS.GetQueries(forceReload=False)
        #Query Results should have a publicQueries and privateQueries section
        self.assertTrue('publicQueries' in qr.keys())
        self.assertTrue('privateQueries' in qr.keys())
        return qr

    def test_FindQuery(self):
        qrList = self.test_GetQueries()
        #There should be at least one Query returned from our cache results
        if (len(qrList) > 0):
            if (len(qrList['publicQueries']) >0):
                randomQueryNum = random.randint(0, len(qrList['publicQueries'])-1)
                qryName = qrList['publicQueries'][randomQueryNum]['name']
                qryId = qrList['publicQueries'][randomQueryNum]['id']
                

                
                qByName = modTFS.FindQueryByName(qryName, RequireLiveData = False)
                qById = modTFS.FindQueryById(qryId, RequireLiveData = False)

                #The WIQL returned should match QueryMethod
                qWiql = qByName['query']
                qMethod = modTFS.QueryMethod(qByName)
                self.assertEqual(qWiql, qMethod, 'The WIQL definition is not identical.')

                self.assertEqual(qById['id'], modTFS.QueryID(qById), 'modTFS.QueryID returned an invalid ID')

                errMsg = "Attempt to find {0} using FindQueryBy{1} failed. Result was {2}"
                self.assertEqual(qById['id'], qryId, errMsg.format(qryId, "Id", str(qById)))
                self.assertEqual(qByName['name'], qryName, errMsg.format(qryName, "Name", str(qByName)))

                
                
        

    def test_GetAFT(self):
        sampleResponse = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">


       <html xmlns="http://www.w3.org/1999/xhtml"><head><title>Microsoft Team Foundation Server
</title><meta http-equiv="X-UA-Compatible" content="IE=10;&#32;IE=9;&#32;IE=8" />

        </head>
<body class=" ">
<input name="__RequestVerificationToken" type="hidden" value="xxxxxxxxxxxxxxxxxxxxx-pjKkIdyxxxXXXXXXXXXXXXXXXhspFBp1yt5cxBnKrfFduLn-VW4Cdxlc5kNB9ytP_25QntpiG5jZBJp45GzmyCa70h37Jlyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" /><input name="__RequestVerificationToken2" type="hidden" value="__RequestVerificationToken2710344ec-32be-42f9-8fb7-xxxxxxxxxxxx" />

    <!-- Shortened data for Unit Testing -->
<div class="main-container"></div></body>
</html>"""
        AFT_TOKEN = modTFS.GetAFT(sampleResponse)
        happyToken = ((len(AFT_TOKEN) > 100) and (len(AFT_TOKEN) < 300))
        self.assertTrue(happyToken) #Token is between 101 and 299 characters. Testing, it may hold steady at 156, but we can be flexible here
        
    def test_ConvertFromTFSDate(self):
        sampleInput = "/Date(1407999345210)/"
        expectedOutput = 1407999345210.0

        d = modTFS.ConvertFromTFSDate(sampleInput)
        self.assertEquals(d, expectedOutput, "modTFS.ConvertFromTFSDate returned {0} but I expected to see {1}".format(d, expectedOutput))


    def test_CleanupTFSPayload(self):
        samplePayload = GenerateSampleData()['payload']
        CleanUpData = modTFS.CleanupTFSPayload(samplePayload, None) #TODO, test Parent functions

        randomID = samplePayload['rows'][3][2]
        cleanID = CleanUpData[3]['System.Id']

        self.assertEqual(randomID, cleanID)


    def test_PayloadDict(self):

        numRows = 100
        sampleData = GenerateSampleData(numRows)
        pd = modTFS.PayloadDictionary(sampleData)
        self.assertEquals(pd['LOG'][0], 'Column Data: Verbose', 'Unepxected data in the Log column was returned. Expected Column Data: Verbose as Log[0]' )
        self.assertEquals(pd['SortedBy'][0], u'System.State', 'SortedBy data is not as expected')
        self.assertEquals(len(pd['payload']), numRows, 'Conversion to payload dictionary does not have enough rows.')
        

        
        
    
if __name__ == '__main__':
    #unittest.main()
    UTSuite = unittest.TestLoader().loadTestsFromTestCase(TestmodTFS)
    unittest.TextTestRunner(verbosity=2).run(UTSuite)
