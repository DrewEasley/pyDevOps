#modCSV

import csv
import StringIO
import os
from modWeb import GetFullDataPath


def ReadCSVStream(stream):

    if (type(stream) == (type(""))):
        datareader = csv.reader(StringIO.StringIO(stream))
        
    else:
        datareader = csv.reader(stream, delimiter=',')

    headers = next(datareader)

    retData = []

    
    HeaderDictionary = {}
    i = 0

    for val in headers:
        HeaderDictionary[i] = val
        i = i+1
    
    
    for row in datareader:
        if len(row) == len(headers):
            dataitem = {}
            for colnum in HeaderDictionary:
                colName = HeaderDictionary[colnum]
                dataitem[colName] = row[colnum]
            retData.append(dataitem)


    
    return retData
    


def ReadFile(filename):
    filename = GetFullDataPath(filename)
    data = open(filename, 'r')
    
    retData = ReadCSVStream(data)
    data.close()
    return retData


def WriteCSV(stream, outfile):
    outfile = GetFullDataPath(outfile)
    fou = open(outfile, 'wb')
    
    headerList = stream[0].keys()
    dw = csv.DictWriter(fou, delimiter=',', fieldnames=stream[0].keys())
    headers = dict( (n,n) for n in stream[0].keys())
    dw.writerow(headers)
    for row in stream:
        dw.writerow(row)
    fou.close()
#x = ReadFile("c:\\devOps\\SFTFSIntegration\\AllOpenBugs.csv")



