import csv
import xlsxwriter 
import os 
import time 

# Opening the CSV files.
class OpenFiles(): 
    def __init__(): 
        day=int(time.strftime("%d"))
        year=time.strftime("%Y")
        monthinteger=int(time.strftime("%m"))
        monthDict={1:'JAN', 2:'FEB', 3:'MAR', 4:'APR', 5:'MAY', 6:'JUN', 7:'JUL', 8:'AUG', 9:'SEP', 10:'OCT', 11:'NOV', 12:'DEC'}
        month= monthDict[monthinteger]
        #Another way to do it 
        #month = datetime.date(1900, monthinteger, 1).strftime('%B')
        #print month

        tu=(day-1,month,year,monthinteger)
    	newdir= os.getcwd()+'\OP Data Sorting {0}{3}{2}'.format(*tu)
        if not os.path.exists(newdir):
    	   os.makedirs(newdir)
    	os.chdir (newdir)
        #Make excel files instead of csv files.. 
    def NewFile1():
            workbook = xlsxwriter.Workbook('OP_Data_Sort_Program_File_1.xlsx') 
        	#Worksheet on OI Data Sort Program File-1
            workbook.add_worksheet('Lot Sizes')

            workbook.add_worksheet('MWPL')

            workbook.add_worksheet('Eq Bhav')

            workbook.add_worksheet('Eq Del')

            workbook.add_worksheet("B'up of Indexes")

            workbook.add_worksheet('Daily OP Data')

            workbook.add_worksheet('BankNifty')

            workbook.add_worksheet('USA Indexes')

            workbook.add_worksheet('Indian Indexes')

            workbook.add_worksheet('Stock-1')

            workbook.add_worksheet('Stock-2')

            workbook.add_worksheet('stock chain-1')

            workbook.add_worksheet('Eq Data Pasting')

            workbook.add_worksheet('FU Data final')

            workbook.add_worksheet('Pasting Data')

            workbook.add_worksheet('Nifty Chain')

            workbook.add_worksheet('Option Chain of All Stock')

            workbook.add_worksheet('Calculation Data')

            workbook.add_worksheet('Gen OI Detail')

            workbook.add_worksheet('All OI Data')
            
            workbook.add_worksheet('Sheet1')

    def NewFile2():
            workbook = xlsxwriter.Workbook('OP_Data_Sort_Program_File_2.xlsx')

            workbook.add_worksheet('Daily OP Data')

            workbook.add_worksheet('Pasting Data')

            workbook.add_worksheet('Stock-3')

            workbook.add_worksheet('Stock-4')

            workbook.add_worksheet('stock chain-2')

            workbook.add_worksheet('Stock-5')

            workbook.add_worksheet('Stock-6')

            workbook.add_worksheet('stock chain-3')

            workbook.add_worksheet('Stock-7')

            workbook.add_worksheet('Stock-8')

            workbook.add_worksheet('stock chain-4')

            workbook.add_worksheet('Stock-9')

            workbook.add_worksheet('Stock-10')

            workbook.add_worksheet('stock chain-5')


    def NewFile3():

        workbook = xlsxwriter.Workbook('OP_Data_Sort_Program_File_3.xlsx')

        workbook.add_worksheet('Daily OP Data')

        workbook.add_worksheet('Pasting Data')

        workbook.add_worksheet('Stock-11')

        workbook.add_worksheet('Stock-12')

        workbook.add_worksheet('stock chain-6')

        workbook.add_worksheet('Stock-13')

        workbook.add_worksheet('Stock-14')

        workbook.add_worksheet('stock chain-7')

        workbook.add_worksheet('Stock-15')

        workbook.add_worksheet('Stock-16')

        workbook.add_worksheet('stock chain-8')

        workbook.add_worksheet('Stock-17')

        workbook.add_worksheet('Stock-18')

        workbook.add_worksheet('stock chain-9')    
    def NewFile4(): 
        workbook = xlsxwriter.Workbook('OP_Data_Sort_Program_File_4.xlsx')

        workbook.add_worksheet('Daily OP Data')

        workbook.add_worksheet('Pasting Data')

        workbook.add_worksheet('Stock-19')

        workbook.add_worksheet('Stock-20')

        workbook.add_worksheet('stock chain-10')

        workbook.add_worksheet('Stock-21')

        workbook.add_worksheet('Stock-22')

        workbook.add_worksheet('stock chain-11')

        workbook.add_worksheet('Stock-23')

        workbook.add_worksheet('Stock-24')

        workbook.add_worksheet('stock chain-12')

        workbook.add_worksheet('Stock-25')

        workbook.add_worksheet('Stock-26')

        workbook.add_worksheet('stock chain-13')      



    #with open('OP_Data_Sort_Program_File_1.csv', 'wb') as fil1:
    #		writer = csv.writer(fil1)
    #with open('OP_Data_Sort_Program_File_2.csv', 'wb') as fil2: 
    #		writer = csv.writer(fil2)
    #with open('OP_Data_Sort_Program_File_3.csv', 'wb') as fil3: 
    #		writer = csv.writer(fil3)
    #with open('OP_Data_Sort_Program_File_4.csv', 'wb') as fil4: 
    #		writer = csv.writer(fil4)		
		#writer.writerows(respData)