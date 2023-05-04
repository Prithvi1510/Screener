import sys
import urllib.request
import csv
import requests
import random
import os
import yfinance as yf
import pandas as pd
from nsetools import Nse
from ColorText import colorText
import json
import platform 
from jsonConfig import jsonConfig
nse = Nse() 


class Tools(): 

    def __init__(self): 
        pass 
    
    def getFromJsonConfig(self,jsonConfig): 
        listStockCodes = [] 
        if(jsonConfig.index == False): 
            listStockCodes = jsonConfig.stockcodes
            return listStockCodes      
        elif(jsonConfig.index == True):
            try: 
                self.checkConnection()
                res  = requests.get(jsonConfig.indexused) 
                cr = csv.reader(res.text.strip().split("\n"))
                next(cr)
                for row in cr: 
                    listStockCodes.append(row[2])
                return listStockCodes
            except Exception as error: 
                print(error)
        else:
            print("Enter a boolean value for index in jsonConfig , true or false")

    #Get the codes from the CSV file present in the CSV file present in nseindia 
    def fetchCodes(self,tickerOption,getFromJson = False): 
        listStockCodes = []

        
        if tickerOption == 12:
            #Gets all the the CODES from Nse india 
            return list(nse.get_stock_codes(cached=False))[1:]
            
            
        tickerMapping = {
            1: "https://archives.nseindia.com/content/indices/ind_nifty50list.csv",
            2: "https://archives.nseindia.com/content/indices/ind_niftynext50list.csv",
            3: "https://archives.nseindia.com/content/indices/ind_nifty100list.csv",
            4: "https://archives.nseindia.com/content/indices/ind_nifty200list.csv",
            5: "https://archives.nseindia.com/content/indices/ind_nifty500list.csv",
            6: "https://archives.nseindia.com/content/indices/ind_niftysmallcap50list.csv",
            7: "https://archives.nseindia.com/content/indices/ind_niftysmallcap100list.csv",
            8: "https://archives.nseindia.com/content/indices/ind_niftysmallcap250list.csv",
            9: "https://archives.nseindia.com/content/indices/ind_niftymidcap50list.csv",
            10: "https://archives.nseindia.com/content/indices/ind_niftymidcap100list.csv",
            11: "https://archives.nseindia.com/content/indices/ind_niftymidcap150list.csv"
        }
    
        if(getFromJson != True):
            try: 
                tickerUrl = tickerMapping.get(tickerOption)
                res  = requests.get(tickerUrl) 
                cr = csv.reader(res.text.strip().split("\n"))
                next(cr)
                for row in cr: 
                    listStockCodes.append(row[2])
            except Exception as error: 
                print(error)
        else: 
            listStockCodes = self.fetchFromWatchList(watchList= False)

        return listStockCodes 

    def fetchStockData(self, stockCode,period,duration):
        data = yf.download(
            tickers = stockCode + ".NS", 
            period= period, 
            interval= duration, 
            progress = False, 
            timeout= 10
        ) 
        return data 
    
    def fetchAllStockData(self, stockCodes,period,duration):
        tickers = [stockCode + ".NS" for stockCode in stockCodes]
        data = yf.download(
            tickers = tickers, 
            period= period, 
            interval= duration, 
            progress = False, 
            timeout= 100
        ) 
        return data 
    
    def fetchLatestNiftyDaily(self, proxyServer=None):
        data = yf.download(
                tickers="^NSEI",
                period='5d',
                interval='1d',
                proxy=proxyServer,
                progress=False,
                timeout=10
            )
        return data 

    # Get Data for Five EMA strategy
    def fetchFiveEmaData(self, proxyServer=None):
        nifty_sell = yf.download(
                tickers="^NSEI",
                period='5d',
                interval='5m',
                proxy=proxyServer,
                progress=False,
                timeout=10
            )
        banknifty_sell = yf.download(
                tickers="^NSEBANK",
                period='5d',
                interval='5m',
                proxy=proxyServer,
                progress=False,
                timeout=10
            )
        nifty_buy = yf.download(
                tickers="^NSEI",
                period='5d',
                interval='15m',
                proxy=proxyServer,
                progress=False,
                timeout=10
            )
        banknifty_buy = yf.download(
                tickers="^NSEBANK",
                period='5d',
                interval='15m',
                proxy=proxyServer,
                progress=False,
                timeout=10
            )
        return nifty_buy, banknifty_buy, nifty_sell, banknifty_sell
    
    def checkConnection(self): 
        try:
            requests.head("http://www.google.com/", timeout=5)
        except requests.ConnectionError:
            print("The internet connection is down")
            sys.exit(1)

    def fetchFromWatchList(self,watchList = False):
        pathWindows = {"watchList" : "\\json\\Custom" , "General" : "\\json\\GeneralStocks" } 
        pathLinux = {"watchList" : "/json/custom" , "General" : "/json/GeneralStocks" }

        watchOption = int(input(colorText.BOLD  +  "1).Fetch from watchList 2).General :" + colorText.END))
        if watchOption == 1: 
            watchList = True

        if watchList == True:  
            if platform.system() == "Windows":
                currentPath = os.getcwd()+pathWindows["watchList"]
            else: 
                currentPath = os.getcwd()+pathLinux["watchList"]
        else: 
            if platform.system() == "Windows": 
                currentPath = os.getcwd()+pathWindows["General"]
            else: 
                currentPath = os.getcwd()+pathLinux["General"]

        json_files = [f for f in os.listdir(currentPath) if f.endswith('.json')]

        if not json_files: 
            print(colorText.BOLD+"No json files" + colorText.END)
            sys.exit(1) 

        for file,index in zip(json_files,range(0,len(json_files))):
            print(colorText.BOLD + colorText.GREEN +"[+]"+str(index)+": "+file+colorText.END)
        
        option = input(colorText.BOLD + colorText.GREEN + "Select Which File: " + colorText.END)

        try: 
            jsonPath = os.path.join(currentPath,json_files[int(option)])
            with open(jsonPath,'r') as json_file: 
                file = json.load(json_file)
                return file["StockCodes"]
        except Exception as exception: 
            print(colorText.BOLD + colorText.FAIL + "Failed To load" + colorText.END)
            print(exception)


    def createJsonFile(self,stockCodeList,filename = "Custom"): 
        if platform.system() == "Windows": 
            currentPath = os.getcwd()+("\\json") 
        else: 
            currentPath = os.getcwd()+("/json/") 
        
        if filename == "Custom": 
            jsonFileName = input(colorText.BOLD + colorText.GREEN + "EnterFileName" + colorText.END)
            jsonFileName += ".json" 
        else: 
            jsonFileName = filename + ".json"

        with open(os.path.join(currentPath, jsonFileName), 'w') as jsonFile: 
            try:
                dictionaryJson = {
                    "StockCodes" :stockCodeList
                    }
                json.dump(dictionaryJson, jsonFile)
                print(colorText.BOLD + colorText.GREEN + "Successfully Created Json file "+ jsonFileName + colorText.END)
            except Exception as e:
                print(colorText.BOLD + colorText.FAIL + "Unsucessfully Created"+ jsonFileName + colorText.END)
                return
        
        return
        



        

                              
