from StringIO import StringIO
from zipfile import ZipFile
import urllib
from urllib import urlopen
from urllib import urlretrieve
testfile=urllib.URLopener()
testfile.retrieve("https://www.nseindia.com/content/historical/EQUITIES/2016/DEC/cm29DEC2016bhav.csv.zip")


#url = urlopen("https://www.nseindia.com/content/historical/EQUITIES/2016/DEC/cm29DEC2016bhav.csv.zip")
#print url.geturl()
#zipfile = ZipFile(StringIO(url.read()))
#for line in zipfile.open(file).readlines():
#    print line



#import urllib2,cookielib
#import csv 
#import zipfile
#site=

#site= "https://www.nseindia.com/content/historical/EQUITIES/2016/DEC/cm29DEC2016bhav.csv.zip"
#hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}

#req = urllib2.Request(site, headers=hdr)

#try:
#    page = urllib2.urlopen(req)
#except urllib2.HTTPError, e:
#    print e.fp.read()
    
#zip_ref=zipfile.ZipFile("C:\Users\arnav\Downloads", 'r') 
#zip_ref.extractall("C:\Users\arnav\Downloads") 
#zip_ref.close()
#content = page.read(2000)
#print content