from secrets import Credentials
from requests_ntlm import HttpNtlmAuth

#WebRequests.py

WebRequests = {}


#This request sends Login data to SalesForce
WebRequests['Salesforce_Login'] = {
    'URL' : 'https://login.salesforce.com',
    'Method': 'POST',
    'Attributes': {
        'un': Credentials['SalesForce']['u'],
        'pw': Credentials['SalesForce']['p']
        }
    }



WebRequests['Salesforce_Report'] = {
    'CACHENAME' : 'SF_REPORT_{0}.sfdat',
    'URL' : 'https://' + Credentials['SalesForce']['i']+ '.salesforce.com/{0}',
    'Method': 'GET',
    'Attributes': {
        'export': 1,
        'enc': 'UTF-8',
        'xf': 'csv'
        }
    
    }


#We need to make an initial connection to TFS to get some necessary information
WebRequests['TFS2010_TEMPLATE'] = {
    'TFSHOME' : Credentials['TFS']['root'],
    'TFSPROJ' : Credentials['TFS']['proj'],
    'Auth': HttpNtlmAuth(Credentials['TFS']['u'], Credentials['TFS']['p']),
    'Method': 'GET' 
    }


