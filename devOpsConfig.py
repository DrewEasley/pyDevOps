#devOps.config.py


#The Test_Designator is used to determine if we are using a Test Environment
#For example, if your Dashboard is deployed to C:\Inetpub\wwwroot
#but the test environment is in C:\Inetpub\wwwroot_test, then the TEST_DESIGNATOR
#should be "_test"




globalConfig = {}

globalConfig['TEST_DESIGNATOR'] = "_test"


globalConfig['SECURITYKEY'] = 'asve@#GKLND><BJ%#@Q:OIJR' #Change this to something else equally unique

#Config settings specific to modWeb only
modWebConfig = {}
modWebConfig['CGIDEBUG_TEST'] = True
modWebConfig['CGIDEBUG_PROD'] = False #Not yet supported, nice to have

