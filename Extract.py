import urllib 
import urllib2
import datetime
import time

def extractfile():

	## dd/mm/yyyy format
	day=int(time.strftime("%d"))
	year=time.strftime("%Y")
	monthinteger=int(time.strftime("%m"))
	print day
	print year
	monthDict={1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
	month= monthDict[monthinteger]
	#Another way to do it 
	#month = datetime.date(1900, monthinteger, 1).strftime('%B')
	print month

	tu=(day-1,month,year)
	url =('https://www.nseindia.com/content/historical/EQUITIES/2016/{1}/cm{0}{1}{2}bhav.csv.zip'.format(*tu))
	print url
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	       'Accept-Encoding': 'none',
	       'Accept-Language': 'en-US,en;q=0.8',
	       'Connection': 'keep-alive'}

	print "downloading with urllib2"
	req = urllib2.Request(url, headers=hdr)
	f = urllib2.urlopen(req)
	data = f.read()
	with open("test5.zip", "wb") as code:
	    code.write(data)

