import urllib
import urllib2
import requests
import zipfile 

url ='https://www.nseindia.com/content/historical/EQUITIES/2016/DEC/cm29DEC2016bhav.csv.zip'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
print "downloading with urllib"
urllib.urlretrieve(url, "code.zip")
zip_ref = zipfile.ZipFile("code.zip",'r')
zip_ref.extractall(C:\Users\arnav\Downloads)

print "downloading with urllib2"
req = urllib2.Request(url, headers=hdr)
f = urllib2.urlopen(req)
data = f.read()
with open("code2.zip", "wb") as code:
    code.write(data)

print "downloading with requests"
r = requests.get(url)
with open("code3.zip", "wb") as code:
    code.write(r.content)

