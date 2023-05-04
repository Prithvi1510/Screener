from decimal import DivisionByZero
from genericpath import isfile
import os
import sys
import platform
import datetime
import pytz
import pickle
import requests
import time
from ColorText import colorText
import pickle 
from Fetcher import Tools


class utility(): 

    def __init__(self): 
        pass    

    def getPath(self,path):  
        if platform.system() == "Windows":
            cwd = os.getcwd()
            return os.path.join(cwd,path)
        else:
            cwd = os.getcwd()
            return os.path.join(os.getcwd(),path)

    def startScreen(self):
        self.clearScreen() 
        option  = input(colorText.BOLD + colorText.GREEN + 
        '''
          1).Load from json file 
          2).Load latest Stocks from CSV
          ''' + colorText.END)  
        if option == '1':
            return True
        elif option == '2': 
            return False 
        else: 
            print(colorText.BOLD + colorText.FAIL + "Wrong Input" + colorText.END )
            return self.startScreen() 
        
    def fetchScreen(self,fetcher,option):
        if option == True:
            return (fetcher.fetchCodes(tickerOption = - 1 ,getFromJson = True)) 
        
        if option == False: 
            print(colorText.BOLD + '''
            1).nifty50list
            2).niftynext50list
            3).nifty100list
            4).nifty200list
            5).nifty500list
            6).niftysmallcap50list
            7).niftysmallcap100list
            8).niftysmallcap250list
            9).niftymidcap50list
            10).niftymidcap100list
            11).niftymidcap150list
            ''' + colorText.END)
            tickerOption = input(colorText.BOLD + "Enter Option: " + colorText.END) 
            return (fetcher.fetchCodes(tickerOption = int(tickerOption),getFromJson = False)) 


    def clearScreen(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')
    
    def savetoCSVfile(self,dataframe): 
        csv_string = 'screened_'+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        try:
            saveToCSV = int(input(colorText.BOLD + "Save screened Stocks To CSV press 1 else Press 0"  + colorText.END))
            if saveToCSV == 1: 
                saveToCSV = True 
            else: 
                saveToCSV = False
        except:
            print(colorText.BOLD + colorText.BOLD + "Enter Integer"+ colorText.END)
            return(self.savetoCSVfile(dataframe= dataframe))
        
        if(saveToCSV == True):
            try:
                dataframe.to_csv(csv_string+'.csv')
                print( colorText.BOLD + colorText.GREEN + 
                    'Created CSV -'+csv_string + colorText.END)
            except OSError as error:
                print(error)
                print(colorText.FAIL + 'Failed to Create CSV ' + colorText.END)
        
    def isTradingTime(self):
        curr = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        openTime = curr.replace(hour=9, minute=15)
        closeTime = curr.replace(hour=15, minute=30)
        return ((openTime <= curr <= closeTime) and (0 <= curr.weekday() <= 4))

    def isClosingHour(self):
        curr = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        openTime = curr.replace(hour=15, minute=00)
        closeTime = curr.replace(hour=15, minute=30)
        return ((openTime <= curr <= closeTime) and (0 <= curr.weekday() <= 4))
    
    def saveAsPickleFile(self, stockDataList): 
        if platform.system() == "Windows": 
            currentPath = os.getcwd()+("\\picklefiles") 
        else: 
            currentPath = os.getcwd()+("/picklefiles/") 

        filename = input( colorText.BOLD + "Enter Filename" + colorText.END)
        filename += ".dat"
        currentPath = os.path.join(filename,filename)
        try: 
            with open(currentPath,"wb") as f: 
                pickle.dump(stockDataList,f) 
        except Exception as e: 
            print(colorText.FAIL + colorText.BOLD + "Failed to create Pickle File"
                   + colorText.END )
            print(e)
            return None

    def loadPickleFile(self): 
        if platform.system() == "Windows": 
            currentPath = os.getcwd()+("\\picklefiles") 
        else: 
            currentPath = os.getcwd()+("/picklefiles/") 
        
        datList = [f for f in os.listdir(currentPath) if f.endswith('.dat')]

        if not datList: 
            print(colorText.BOLD+"No Dat files" + colorText.END)
            return 

        for file,index in zip(datList,range(1,len(datList))):
            print(colorText.BOLD + colorText.GREEN +"[+]"+str(index)+": "+file+colorText.END)
        
        option = input(colorText.BOLD + colorText.GREEN + "Select Which File: " + colorText.END)

        try: 
            picklePath = os.path.join(currentPath,datList[int(option)])
            with open(picklePath, 'r') as pickleFile: 
                stockDataList = pickleFile.load(pickleFile)
                return stockDataList
        except Exception as error: 
            print(colorText.FAIL + colorText.BOLD + "Failed to Load Pickle File"
                   + colorText.END )
            print(error)
            sys.exit(1)
                               


        
    


    



     