#modDataCache
import cPickle as picl
import os
from modWeb import GetFullDataPath

import hmac
from devOpsConfig import globalConfig

#import deepDataDictionary


debugVerbose = globalConfig['VERBOSITY']

def CacheName(modName, obj):
    
    if (obj is None):
        return None
    
    #Stringify our input
    if (type(obj) <> type("")):
        obj = str(obj)

    nameTemplate = "{0}_{1}.picl"  #TFS_SomeData.picl

    #Generate a hash value
    secKey = globalConfig['SECURITYKEY']
    h = hmac.new(secKey)
    h.update(obj)

    objhash = h.hexdigest()
    
    cacheName = nameTemplate.format(modName, objhash)
    return cacheName

def CacheFile(modName, obj):
    cn = CacheName(modName, obj)
    fn = GetFullDataPath(cn)
    return fn
    
def SaveToCache(SendingMod, r, d):
    #R is the request object
    #d is the actual data
    fn = CacheFile(SendingMod, r)
    picl.dump(d, open(fn, "wb"))
    if (debugVerbose):
        print " ***** NEW RESULT SAVING *****"
        print fn
        print globalConfig['SECURITYKEY']
        print SendingMod
        print r


def LoadFromCache(RequestingMod, r):
    fn = CacheFile(RequestingMod, r)
    if (os.path.exists(fn)):
        d = picl.load( open(fn, "rb"))
        return d
    else:
        if (debugVerbose):
            print "**** LoadfromCache not found ****"
            print fn
            print globalConfig['SECURITYKEY']
            print RequestingMod
            print r
        return None



