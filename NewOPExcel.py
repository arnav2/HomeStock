import xlrd as xl
import xlsxwriter 
import os 
import time 
import numpy as np 
# Opening the CSV files.
class OpenFiles(): 
    def __init__(self): 
        ##This should be put in time file... 
        day=int(time.strftime("%d"))
        year=time.strftime("%Y")
        monthinteger=int(time.strftime("%m"))
        monthDict={1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
        month= monthDict[monthinteger]
        #Another way to do it 
        #month = datetime.date(1900, monthinteger, 1).strftime('%B')
        
        tu=(day,month,year,monthinteger)
    	
        #Making a directory.. 
        newdir= os.getcwd()+'\OP Data Sorting {0}{3}{2}'.format(*tu)
        if not os.path.exists(newdir):
    	   os.makedirs(newdir)
        #Changing or writing in that directory.. 
    	os.chdir (newdir)

        self.worksheetdict=[]

        self.worksheetdict.append(['Lot Sizes','MWPL','Eq Bhav','Eq Del',"B'up of Indexes",
        'Daily OP Data','BankNifty','USA Indexes','Indian Indexes','Stock-1',
        'Stock-2','stock chain-1','Eq Data Pasting','FU Data final',
        'Pasting Data','Nifty Chain','Option Chain of All Stock',
        'Calculation Data','Gen OI Detail','All OI Data','Sheet1'])
        
        self.worksheetdict.append(['Daily OP Data','Pasting Data','Stock-3','Stock-4',
                        'stock chain-2','Stock-5','Stock-6','stock chain-3',
                        'Stock-7','Stock-8','stock chain-4','Stock-9',
                        'Stock-10','stock chain-5'])

        self.worksheetdict.append(['Daily OP Data','Pasting Data','Stock-11','Stock-12',
                    'stock chain-6','Stock-13','Stock-14','stock chain-7',
                    'Stock-15','Stock-16','stock chain-8','Stock-17',
                    'Stock-18','stock chain-9'])

        self.worksheetdict.append(['Daily OP Data','Pasting Data','Stock-19','Stock-20',
                    'stock chain-10','Stock-21','Stock-22','stock chain-11',
                    'Stock-23','Stock-24','stock chain-12','Stock-25',
                    'Stock-26','stock chain-13']) 
        
        print self.worksheetdict

        self.workbook=[]
        self.worksheet=[]
        
        for i in range(0,4):   
            self.workbook.append(xlsxwriter.Workbook('OP_Data_Sort_Program_File_'+str(i+1)+'.xlsx')) 
            #To make a list of lists 
            self.worksheet.append([])
            
            for j in range(0,len(self.worksheetdict[i])-1):
                self.worksheet[i].append(self.workbook[i].add_worksheet((self.worksheetdict[i])[j]))    

    def NewFile1(self):
        
        ##Reads Data from a file very easily... XLRD might be useful in the future. 
        #TeamPointWorkbook = xl.open_workbook('OP_Data_Sort_Program_File_1.xlsx')       
        #pointSheets = TeamPointWorkbook.sheet_names()
        print pointSheets
            #print len(sheet)

    def NewFile2(self):
#Just make a loop instead that loops through all the names in workbook 2 and puts in a new worksheet. 
#Then work with each worksheet in a different file 
#Use if else condition from a worksheet name. 
            
            


        print "shit"

    def NewFile3(self):
#Just make a loop instead that loops through all the names in workbook 3
# and puts in a new worksheet. 
#Then work with each worksheet in a different file 
#Use if else condition from a worksheet name. 
       
        print "shit"    
  
    def NewFile4(self): 
        print "shit"
#Just make a loop instead that loops through all the names in workbook 4
# and puts in a new worksheet. 
#Then work with each worksheet in a different file 
#Use if else condition from a worksheet name. 
        
    def __enter__(self):
        return self
    
    def __exit__(self,exc_type, exc_value, traceback):
        for i in range(0,len(self.workbook)-1): 
            self.workbook[i].close()

with OpenFiles() as xyz:
    xyz.NewFile1()