from Fetcher import Tools
import numpy as np
import pandas as pd
from Config import config  
from Screener import screener 
from candlePatterns import CandlePatterns
from Config import config 
from utility import utility 
from ColorText import colorText
import os 
import datetime
import sys
import json
from utility import utility 
from jsonConfig import jsonConfig
import configparser 
from Config import config 
from alive_progress import alive_bar
from stockData import stockData 
from plotter import Plotter
import matplotlib.pyplot as plt 


parser = configparser.ConfigParser(strict=False)
Screener = screener() 
defaultConfig = config()
fetcher = Tools()
utils = utility() 
stockArrary = [] 
stockDictionary = {}
index = 0

defaultConfig.getConfig(parser = parser)
json = jsonConfig(defaultConfig= defaultConfig)
stockCodes = fetcher.getFromJsonConfig(jsonConfig = json)

#StockCodes = utils.fetchScreen(fetcher = fetcher ,option = utils.startScreen())


with alive_bar(len(stockCodes)) as bar :
    for stock in stockCodes:
        stockArrary.append(stockData(stockCode= stock,config=defaultConfig,fetcher = fetcher, screener= Screener)) 
        stockDictionary[stock] = index
        index += 1 
        bar() 


fig = Plotter().show(stockArrary[2],trimmed = True)
plt.show() 


# parser = configparser.ConfigParser(strict=False)
# config1 = config()
# config1.getConfig (parser = parser)
# json = jsonConfig(defaultConfig= config1)

# print(json.index)
# print(json.stockcodes)
# print(json.indexUsed)
# utils.fetchScreen(fetcher = Fetcher ,option = utils.startScreen())

# fulldata,trimmeddata = screener().preprocessData(data=Data,configManager= configManager)
# StockCodes = Tools().fetchCodes(tickerOption= 1)
# print(fulldata,trimmeddata)
# for ticker in StockCodes: 
#     config().setConfig(default= True )
#     Data = Tools().fetchStockData(stockCode=  ticker,period = configManager.period,duration=configManager.duration)
#     fulldata,trimmeddata = screener().preprocessData(data= Data,configManager=configManager)
#     CandlePatterns().findPattern(data = trimmeddata, dict = {}, saveDict= {} ) 
#     utility().clearScreen


# for i in range(1,11): 
#     filenameList = ["afddsf","ind_nifty50list","ind_niftynext50list"
#                     ,"ind_nifty100list","ind_nifty200list",
#                     "ind_nifty500list","ind_niftysmallcap50list",
#                     "ind_niftysmallcap100list","ind_niftysmallcap250list",
#                     "ind_niftymidcap50list","ind_niftymidcap100list",
#                     "ind_niftymidcap150list"
#                     ]
    
   
#     stockCodes = Tools().fetchCodes(tickerOption= int(i)) 
#     print("stockCodes:",str(i),stockCodes)
#     Tools().createJsonFile(stockCodeList= stockCodes, filename = filenameList[i])




# file = 'C:\\Users\\ultim\\OneDrive\\Desktop\\screener\\json\\mickey.json'
# with open(file,'r') as f:
#    data = json.load(f)

# print(data)
# Tools().fetchFromWatchList()
# csv_string = 'screened_'+datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")+'.csv'
# nme = ["aparna", "pankaj", "sudhir", "Geeku"]
# deg = ["MBA", "BCA", "M.Tech", "MBA"]
# scr = [90, 40, 80, 98]
 
# # dictionary of lists
# stockData.screenDict = {'name': nme, 'degree': deg, 'score': scr}
     
# df = pd.DataFrame(stockData.screenDict)
 
# print(df)
# df.to_csv(csv_string)



# df1 = pd.DataFrame([{"stock" : "MOS", "condition" : True}], index = [0]) 
# df2 = pd.DataFrame([{"stock" : "MOS2", "condition" : False}],index= [1])
# df3 =  df1.append(df2) 
# print(df3)
# # data1 = {
#   "age": [16, 14, 10],
#   "qualified": [True, True, True]
# }
# df1 = pd.DataFrame(data1)

# data2 = {
#   "age": [55, 40],
#   "qualified": [True, False]
# }
# df2 = pd.DataFrame(data2)

# newdf = df1.append(df2)
# print(newdf)


# import sys 
# import math 
# import numpy as np 
# import pandas as pd  
# import talib  
# import datetime as dt
# from ColorText import colorText
# from candlePatterns import CandlePatterns


# class screener: 
    
#     def __init__(self) -> None:
#         pass
    
#     # Private method to find candle type
#     # True = Bullish, False = Bearish
#     def getCandleType(self, dailyData):
#         return bool(dailyData['Close'][-1] >= dailyData['Open'][-1])
    

#     def preprocessData(self,data,configManager ):
#         if configManager.daysToLookback == None: 
#             daysToLookback = configManager.daysToLookback
#         else: 
#             daysToLookback = 30

#         if configManager.useEMA: 
#             sma = talib.EMA(data['Close'], timeperiod = 50  ) 
#             lma = talib.EMA(data['Close'],timeperiod =200)  
#         else: 
#             sma = data.rolling(window = 50).mean() 
#             lma = data.rolling(window = 200).mean() 
#             data.insert(6,'SMA',sma['Close'])
#             data.insert(7,'LMA',lma['Close'])
#             vol = data.rolling(window=20).mean()
#             rsi = talib.RSI(data['Close'], timeperiod=14)
#             data.insert(8,'VolMA',vol['Volume'])
#             data.insert(9,'RSI',rsi)
#             data = data[::-1]               # Reverse the dataframe
#             # data = data.fillna(0)
#             # data = data.replace([np.inf, -np.inf], 0)
#             fullData = data
#             trimmedData = data.head(daysToLookback)
#             return fullData, trimmedData
        

#     def runScreener(self,data,screenerFunction,stockCode):
#         #when passing function pass df to screener
#         df = data 
#         screenDataFrame = pd.DataFrame(screenerFunction(df,stockCode)) 


#     def validateMovingAverages(self, data, screenDict, saveDict, maRange=2.5):
#         data = data.fillna(0)
#         data = data.replace([np.inf, -np.inf], 0)
#         recent = data.head(1)
#         if(recent['SMA'][0] > recent['LMA'
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + 'Bullish' + colorText.END
#             saveDict['MA-Signal'] = 'Bullish'
#         elif(recent['SMA'][0] < recent['LMA'][0]):
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + 'Bearish' + colorText.END
#             saveDict['MA-Signal'] = 'Bearish'
#         elif(recent['SMA'][0] == 0):
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.WARN + 'Unknown' + colorText.END
#             saveDict['MA-Signal'] = 'Unknown'
#         else:
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.WARN + 'Neutral' + colorText.END
#             saveDict['MA-Signal'] = 'Neutral'

#         smaDev = data['SMA'][0] * maRange / 100
#         lmaDev = data['LMA'][0] * maRange / 100
#         open, high, low, close, sma, lma = data['Open'][0], data['High'][0], data['Low'][0], data['Close'][0], data['SMA'][0], data['LMA'][0]
#         maReversal = 0
#         # Taking Support 50
#         if close > sma and low <= (sma + smaDev):
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + '50MA-Support' + colorText.END
#             saveDict['MA-Signal'] = '50MA-Support'
#             maReversal = 1
#         # Validating Resistance 50
#         elif close < sma and high >= (sma - smaDev):
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + '50MA-Resist' + colorText.END
#             saveDict['MA-Signal'] = '50MA-Resist'
#             maReversal = -1
#         # Taking Support 200
#         elif close > lma and low <= (lma + lmaDev):
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + '200MA-Support' + colorText.END
#             saveDict['MA-Signal'] = '200MA-Support'
#             maReversal = 1
#         # Validating Resistance 200
#         elif close < lma and high >= (lma - lmaDev):
#             screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + '200MA-Resist' + colorText.END
#             saveDict['MA-Signal'] = '200MA-Resist'
#             maReversal = -1
#         # For a Bullish Candle
#         if self.getCandleType(data):
#             # Crossing up 50
#             if open < sma and close > sma:
#                 screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + 'BullCross-50MA' + colorText.END
#                 saveDict['MA-Signal'] = 'BullCross-50MA'
#                 maReversal = 1            
#             # Crossing up 200
#             elif open < lma and close > lma:
#                 screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + 'BullCross-200MA' + colorText.END
#                 saveDict['MA-Signal'] = 'BullCross-200MA'
#                 maReversal = 1
#         # For a Bearish Candle
#         elif not self.getCandleType(data):
#             # Crossing down 50
#             if open > sma and close < sma:
#                 screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + 'BearCross-50MA' + colorText.END
#                 saveDict['MA-Signal'] = 'BearCross-50MA'
#                 maReversal = -1         
#             # Crossing up 200
#             elif open > lma and close < lma:
#                 screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + 'BearCross-200MA' + colorText.END
#                 saveDict['MA-Signal'] = 'BearCross-200MA'
#                 maReversal = -1
#         return maReversal
    
#     def validateVolume(self, data, screenDict, saveDict, volumeRatio=2.5):
#         data = data.fillna(0)
#         data = data.replace([np.inf, -np.inf], 0)
#         recent = data.head(1)
#         if recent['VolMA'][0] == 0: # Handles Divide by 0 warning
#             saveDict['Volume'] = "Unknown"
#             screenDict['Volume'] = colorText.BOLD + colorText.WARN + "Unknown" + colorText.END
#             return True
#         ratio = round(recent['Volume'][0]/recent['VolMA'][0],2)
#         saveDict['Volume'] = str(ratio)+"x"
#         if(ratio >= volumeRatio and ratio != np.nan and (not math.isinf(ratio)) and (ratio != 20)):
#             screenDict['Volume'] = colorText.BOLD + colorText.GREEN + str(ratio) + "x" + colorText.END
#             return True
#         screenDict['Volume'] = colorText.BOLD + colorText.FAIL + str(ratio) + "x" + colorText.END
#         return False

    

#     def MarkMinevini(self,df,screenDict, saveDict): 
#         '''
#         Use original Data 
#         The current stock price is above both the 150-day and 200-day moving average
#         The 150-day moving average is above the 200-day moving average
#         The 200-day moving average is trending up for at least 1 month
#         The 50-day moving average is above both the 150-day and 200-day moving average
#         The current stock price is trading above the 50-day moving average
#         The current stock price is at least 30% above it’s 52-week low
#         The current stock price is within at least 25% of it’s 52-week high
#         The relative strength ranking (in IBD) is no less than 70, preferably in the 80’s or 90’s
#         '''
#         df['SMA_200'] = df['Adj Close'].rolling(200).mean()
#         df['SMA_150'] = df['Adj Close'].rolling(150).mean()
#         df['SMA_50'] = df['Adj Close'].rolling(50).mean()
        
#         # Determine the 52 week high and low
#         low_of_52week=min(df["Adj Close"][-260:])
#         high_of_52week=max(df["Adj Close"][-260:])

#         # Storing required values 
#         currentClose = df["Adj Close"][-1]
#         moving_average_50 = df["SMA_50"][-1]
#         moving_average_150 = df["SMA_150"][-1]
#         moving_average_200 = df["SMA_200"][-1]
#         low_of_52week = round(min(df["Low"][-260:]), 2)
#         high_of_52week = round(max(df["High"][-260:]), 2)
#         RSI = round(talib.RSI(df['Adj Close'] , timeperiod = 12),2) 

#         try: 
#             moving_average_200_20 = df["SMA_200"][-20]
#         except Exception: 
#             moving_average_200_20 = 0 
#         #Condition 1: Current Price > 150 SMA and > 200 SMA
#         condition_1 = currentClose > moving_average_150 > moving_average_200
#         # Condition 2: 150 SMA and > 200 SMA
#         condition_2 = moving_average_150 > moving_average_200
#         # Condition 3: 200 SMA trending up for at least 1 month
#         condition_3 = moving_average_200 > moving_average_200_20
#         # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
#         condition_4 = moving_average_50 > moving_average_150 > moving_average_200 
#         # Condition 5: Current Price > 50 SMA
#         condition_5 = currentClose > moving_average_50 
#         # Condition 6: Current Price is at least 30% above 52 week low
#         condition_6 = currentClose >= (1.3*low_of_52week) 
#         # Condition 7: Current Price is within 25% of 52 week high
#         condition_7 = currentClose >= (.75*high_of_52week)
#         #conditon 8: RSI(maybe) > 70 
#         condition_8 = RSI > 70.00
#         condition = (condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7 and condition_8) 

#         if condition == True: 
#             screenDict["MarkMinerviTemplate"] = colorText.BOLD + colorText.GREEN + 'Yes' + colorText.END
#             saveDict["MarkMinerviTemplate"] = "Yes"
#         else: 
#             screenDict["MarkMinerviTemplate"] = colorText.BOLD + colorText.FAIL + 'No' + colorText.END
#             saveDict["MarkMinerviTemplate"] = "No"

#     def dictScreener(self): 
#         print(colorText.BOLD + colorText.WARN + 
#               """Enter your option
#               [+] 1)> MarkMinveri Template 
#               [+] 2)> Moving Averages 
#               [+] 3)> Validate Volumes 
#               [+] 4)> Candle Pattern 
#               [+] 5)> All Patterns 
#               """
#              +colorText.END )
#         screenerClass = screener()
#         CandlePatternsClass = CandlePatterns()
#         option = int(input(colorText.BOLD + colorText.WARN + "Enter option" + colorText.END ))
#         screenerFunction = ({1: screenerClass.MarkMinevini , 2: screenerClass.validateVolume , 3: screenerClass.validateMovingAverages, 
#                              4: CandlePatternsClass.findPattern })
        
#         try: 
#             function = screenerFunction[option]
#             return function 
#         except KeyError:
#             print(colorText.BOLD + colorText.FAIL + 'INVALID OPTION' + colorText.END)
#             sys.exit(0) 
            

#NEW -----------------------------------------------------------------------------------------------
# from candlePatterns import CandlePatterns
# from Fetcher import Tools 
# from Config import config
# from ColorText import colorText 
# from utility import utility
# from Screener import screener
# from alive_progress import alive_bar
# from stockData import stockData
# import pandas as pd 

# Screener = screener() 
# defaultConfig = config()
# fetcher = Tools()
# utils = utility() 
# StockCodes = fetcher.fetchCodes(tickerOption= 1)
# stockArrary = [] 
# stockDictionary = {}
# index = 0

# with alive_bar(len(StockCodes)) as bar :
#     for stock in (StockCodes):
#         stockArrary.append(stockData(stockCode= stock,config=defaultConfig,fetcher = fetcher, screener= Screener)) 
#         stockDictionary[stock] = index
#         index += 1 
#         bar() 

# while(True):
#     print(
#         '''
#         Enter Option 
#         1). Screen Stock 
#         2).Show Stock 
#         '''
#     )
#     option = int(input(colorText.BOLD + colorText.GREEN + "Enter option: " + colorText.END))
#     if(option == 1): 
#         function = Screener.dictScreener()
#         print(colorText.BOLD + colorText.GREEN
#             +"Screening Each Stock" +  colorText.END) 
#         with alive_bar(len(stockArrary)) as bar:
#             #stockElement is Class StockData 
#             for stockElement in stockArrary:
#                 stockElement.applyScreener(screeners = function)
#                 bar()
#         screenDictList,pandaIndex = [] , 0 
#         for stockElement in (stockArrary):
#             #stockElement.saveDict.add("StockCode",str(stockElement.StockCode))
#             screenDictList.append(stockElement.saveDict)
#         #print(screenDictList)
#         screenDataframe = pd.DataFrame(screenDictList) 
#         print(screenDataframe)
#         utils.savetoCSVfile(screenDataframe)
#     else:
#         print(stockDictionary.keys())
#         stockCheck = input(colorText.BOLD + colorText.GREEN + "Enter The Stock Code" + colorText.END)

#         try:
#             stockArraryIndex = stockDictionary[stockCheck]
#             print(stockArrary[stockArraryIndex].trimmedData)
#         except Exception as e:
#             print(e)
#             print("No Stock Code found")
        
        

# #OLD CODE -------------------------------------------------------------------------------------------
# from candlePatterns import CandlePatterns
# from Fetcher import Tools 
# from Config import config
# from ColorText import colorText 
# from utility import utility
# from Screener import screener
# from alive_progress import alive_bar
# from stockData import stockData
# import pandas as pd 


# Screener = screener() 
# defaultConfig = config()
# fetcher = Tools()
# utils = utility() 
# StockCodes = fetcher.fetchCodes(tickerOption= 1)
# stockArrary = [] 

# with alive_bar(len(StockCodes)) as bar :
#     for stock in StockCodes:
#         stockArrary.append(stockData(stockCode= stock,config=defaultConfig,fetcher = fetcher, screener= Screener)) 
#         bar() 

# function = Screener.dictScreener()

# print(colorText.BOLD + colorText.GREEN
#       +"Screening Each Stock" +  colorText.END) 
# with alive_bar(len(stockArrary)) as bar:
#     #stockElement is Class StockData 
#     for stockElement in stockArrary:
#         stockElement.applyScreener(screeners = function)
#         bar()

# screenDictList,pandaIndex = [] , 0 

# for stockElement in (stockArrary):
#     #stockElement.saveDict.add("StockCode",str(stockElement.StockCode))
#     screenDictList.append(stockElement.saveDict)

# #print(screenDictList)
# screenDataframe = pd.DataFrame(screenDictList) 
# print(screenDataframe)
# utils.savetoCSVfile(screenDataframe)


# def fetchFromWatchList(self,watchList = False):
#     pathWindows = {"watchList" : "\\json\\Custom" , "General"}
#     if platform.system() == "Windows": 
#         currentPath = os.getcwd()+("\\json") 
#     else: 
#         currentPath = os.getcwd()+("/json/") 
#     json_files = [f for f in os.listdir(currentPath) if f.endswith('.json')]

#     if not json_files: 
#         print(colorText.BOLD+"No json files" + colorText.END)
#         sys.exit(1) 

#     for file,index in zip(json_files,range(0,len(json_files))):
#         print(colorText.BOLD + colorText.GREEN +"[+]"+str(index)+": "+file+colorText.END)
    
#     option = input(colorText.BOLD + colorText.GREEN + "Select Which File: " + colorText.END)

#     try: 
#         jsonPath = os.path.join(currentPath,json_files[int(option)])
#         with open(jsonPath,'r') as json_file: 
#             file = json.load(json_file)
#             return file["StockCodes"]
#     except Exception as exception: 
#         print(colorText.BOLD + colorText.FAIL + "Failed To load" + colorText.END)
#         print(exception)
