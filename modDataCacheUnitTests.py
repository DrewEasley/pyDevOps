#modDataCacheUnitTests.py

import unittest

from devOpsConfig import globalConfig
import modDataCache
import os

class TestmodDataCache(unittest.TestCase):
    def setUp(self):
        #We need to override this temporarily
        globalConfig['SECURITYKEY'] = 'UnitTesting123'

        self.TESTOBJECT1 = 'My String Value'
        self.TESTOBJECT2 = ['C', 'o', 'f', 'f', 'e', 'e']
        self.TESTOBJECT3 = {'RequestMoreCoffee': True,
              'CoffeeType': 'PourOver',
              'TastesLike': ['Apples', 'Cherries']}
        

    def TestCacheName(self, o1, o1_expect):
        o1_actual = modDataCache.CacheName('UnitTest', o1)
        errText = "Cache value should have been {0} but was actually {1}"
        self.assertEqual(o1_actual, o1_expect, errText.format(o1_expect, o1_actual))
    

    def test_CacheNameByString(self):
        o1 = self.TESTOBJECT1 
        o1_expect = 'UnitTest_8f0a5640084885b1dc144b9814f655d2.picl'
        self.TestCacheName(o1, o1_expect)
        
        
        

    def test_CacheNameByList(self):
        o1 = self.TESTOBJECT2
        o1_expect = "UnitTest_f6615ffcc859b5da2f160fda13e051db.picl"
        self.TestCacheName(o1, o1_expect)
        

    def test_CacheNameByDict(self):
        o1 = self.TESTOBJECT3
        o1_expect = "UnitTest_0dfc402d3d186df1c9b2f7df87ecde51.picl"
        
        self.TestCacheName(o1, o1_expect)

    def test_CacheNameFailure(self):
        o1 = None
        o1_expect = None
        self.TestCacheName(o1, o1_expect)
        

    def test_CacheFileFullPath(self):
        cFileName = modDataCache.CacheFile("UnitTest", self.TESTOBJECT1)
        self.assertTrue(len(os.path.split(cFileName)) > 1) #Full path should have multiple parts


    def test_CacheObject3(self):
        modDataCache.SaveToCache("UnitTest", self.TESTOBJECT2, self.TESTOBJECT3)
        res = modDataCache.LoadFromCache("UnitTest", self.TESTOBJECT2)
        self.assertEquals(self.TESTOBJECT3, res)

    def test_CacheObjectNotFound(self):
        res = modDataCache.LoadFromCache("UnitTest", "Gobbleygook")
        self.assertEquals(None, res)

if __name__ == '__main__':
    #unittest.main()
    UTSuite = unittest.TestLoader().loadTestsFromTestCase(TestmodDataCache)
    unittest.TextTestRunner(verbosity=2).run(UTSuite)
