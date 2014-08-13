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
WebRequests['TFS_QUERYROOT'] = {
    'URL': "{0}{1}{2}",
    'PROJ': Credentials['TFS']['proj'],
    'ROOT': Credentials['TFS']['root'],
    'Method': 'GET',
    'PREVENTCACHING': True,
    'Auth': HttpNtlmAuth(Credentials['TFS']['u'], Credentials['TFS']['p'])
    }


WebRequests['TFS_QUERIES'] = {
    'URL': Credentials['TFS']['root'] + Credentials['TFS']['proj'] + '_api/_wit/queries',
    'Method': 'GET',
    'PREVENTCACHING': True,
    'Attributes': {
        '__v': 1,
        'includeQueryTexts': 'true'
        },
        
    'Auth': HttpNtlmAuth(Credentials['TFS']['u'], Credentials['TFS']['p'])
    }


WebRequests['TFS_QUERY'] = {
    'CACHENAME': 'TFS_QUERY_{0}.tfsdat',
    'URL': "{0}{1}{2}" ,
    'Method': 'POST',
    'Headers': {
        'content-type': 'application/x-www-form-urlencoded'
        },
    'Attributes': {
        
        'runQuery': True,
        'wiql' : ""
        },
        
    'Auth': HttpNtlmAuth(Credentials['TFS']['u'], Credentials['TFS']['p'])
    }


