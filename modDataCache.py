#modDataCache
import cPickle as picl
import os
from modWeb import GetFullDataPath

import hmac
from devOpsConfig import globalConfig

def CacheName(modName, obj):
    
    if (obj is None):
        return None
    
    #Stringify our input
    if (type(obj) <> type("")):
        obj = str(obj)

    nameTemplate = "{0}_{1}.picl"  #TFS_SomeData

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
    
def SaveToCache(SendingMod, d):
    fn = CacheFile(SendingMod, d)
    picl.dump(d, open(fn, "wb"))


def LoadFromCache(RequestingMod, d):
    fn = CacheFile(RequestingMod, d)
    if (os.path.exists(fn)):
        d = picl.load( open(fn, "rb"))
        return d
    else:
        return None

