import urllib2
import datetime
import time
import re
import csv
import os
from Unzip import ExtractAll

## dd/mm/yyyy format
class ExtractFiles():
	#self , argument should be put as arguments... 
	def __init__() :
		print "Starting the Extraction process.... " 
	 
		day=int(time.strftime("%d"))
		year=time.strftime("%Y")
		monthinteger=int(time.strftime("%m"))
		monthDict={1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
		month= monthDict[monthinteger]
		#Another way to do it 
		#month = datetime.date(1900, monthinteger, 1).strftime('%B')
		print month

		tu=(day-1,month,year,monthinteger)
		url =('https://www.nseindia.com/content/historical/EQUITIES/{2}/{1}/cm{0}{1}{2}bhav.csv.zip'.format(*tu))
		url2=('https://www.nseindia.com/content/historical/DERIVATIVES/{2}/{1}/fo{0}{1}{2}bhav.csv.zip'.format(*tu))
		url3=('https://www.nseindia.com/archives/nsccl/mwpl/combineoi_{0}{3}{2}.zip'.format(*tu))
		url4=('https://www.nseindia.com/archives/equities/mto/MTO_{0}{3}{2}.DAT'.format(*tu))

		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

		print "downloading with urllib2"

####### Please check if it exists.
####### The program will automatically see the file in an hour. 

####### ERROR 1 should throw an error that the file bhavcopy was not opened. 
	def Downloading():

		try: 
			req = urllib2.Request(url, headers=hdr)
			f = urllib2.urlopen(req)
			data = f.read()
			with open("test5.zip", "wb") as code:
			    code.write(data)

		except urllib2.HTTPError as err:
			if err.code == 404: 
				print " Error 1"

		####### ERROR 2 should throw the path of the file bhavcopy was not opened.

		try:
			req2 = urllib2.Request(url2, headers=hdr)
			f2 = urllib2.urlopen(req2)
			data2 = f2.read()
			with open("test6.zip", "wb") as code:
			    code.write(data2)

		except urllib2.HTTPError as err:
			if err.code == 404: 
				print " Error 2"

		######	ERROR 3 should prompt the user that the file 3 path was not opened. 
		try: 
			req3 = urllib2.Request(url3, headers=hdr)
			f3 = urllib2.urlopen(req3)
			data3 = f3.read()
			with open("test7.zip", "wb") as code:
			    code.write(data3)
		except urllib2.HTTPError as err:
			if err.code == 404: 
				print " Error 3"	 
		#####Similarly Error 4 should also throw the error 
		try: 
			req4 = urllib2.Request(url4,headers=hdr)
			resp4 = urllib2.urlopen(req4)
			respData = resp4.read()
			print respData
			file = open("newfile.txt", "w")
			file.write(respData)
			file.close()
		except urllib2.HTTPError as err:
			if err.code == 404: 
				print " Error 4"	 
		####IF both error 3 and error 4 does not open then prompt the user 
		#### check if archives folder exist or not.  
		
	#Extracting all the files.. 
	def Extracting(): 
		ExtractAll()
	# Opening the CSV files. 
	def OpenNewCSV(): 
		newdir= os.getcwd()+'\OP Data Sorting {0}{3}{2}'.format(*tu)
		os.makedirs(newdir)
		os.chdir (newdir)
		#with open():

		with open('somefile.csv', 'wb') as file:
	    		writer = csv.writer(file)

    		#writer.writerows(respData)