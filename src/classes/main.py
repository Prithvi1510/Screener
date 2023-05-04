from candlePatterns import CandlePatterns
from Fetcher import Tools 
from Config import config
from ColorText import colorText 
from utility import utility
from Screener import screener
from alive_progress import alive_bar
from stockData import stockData
import pandas as pd 
import configparser 
from jsonConfig import jsonConfig 

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

while(True):
    print(
        '''
        Enter Option 
        1). Screen Stock 
        2). Show Stock 
        '''
    )
    option = int(input(colorText.BOLD + colorText.GREEN + "Enter option: " + colorText.END))
    if(option == 1): 
        function = Screener.dictScreener()
        print(colorText.BOLD + colorText.GREEN
            +"Screening Each Stock" +  colorText.END) 
        with alive_bar(len(stockArrary)) as bar:
            #stockElement is Class StockData 
            for stockElement in stockArrary:
                stockElement.applyScreener(screeners = function)
                bar()
        screenDictList,pandaIndex = [] , 0 
        for stockElement in (stockArrary):
            #stockElement.saveDict.add("StockCode",str(stockElement.StockCode))
            screenDictList.append(stockElement.saveDict)
        #print(screenDictList)
        screenDataframe = pd.DataFrame(screenDictList) 
        print(screenDataframe)
        utils.savetoCSVfile(screenDataframe)
    else:
        print(stockDictionary.keys())
        stockCheck = input(colorText.BOLD + colorText.GREEN + "Enter The Stock Code" + colorText.END)

        try:
            stockArraryIndex = stockDictionary[stockCheck]
            print(stockArrary[stockArraryIndex].trimmedData)
        except Exception as e:
            print(e)
            print("No Stock Code found")


