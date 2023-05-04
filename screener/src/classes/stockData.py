from candlePatterns import CandlePatterns
from Fetcher import Tools 
from Config import config
from ColorText import colorText 
from utility import utility
from Screener import screener
from alive_progress import alive_bar
import pandas as pd 



class stockData(): 

    def __init__(self,stockCode,config,fetcher,screener):
        self.stockCode = stockCode
        self.saveDict = {"StockCode":str(self.stockCode)}
        self.screenDict = {"StockCode":str(self.stockCode)} 
        self.config = config 
        self.data = fetcher.fetchStockData(stockCode = self.stockCode ,
                                           period = self.config.period ,duration = self.config.duration)
        self.fullData ,self.trimmedData = screener.preprocessData(data = self.data, 
                                                                  configManager = self.config )
        
    def applyScreener(self,screeners): 
        #apply every screener in the queue
        for screener in screeners: 
            screener(stockData = self )
    
    def filterStockData(self,filterList,stockDataList): 
        #filter list will be dictionary loaded from json file 
        filteredDataList = []
        for filter in filterList:
            for stockData in stockDataList:
                if (stockData.stockCode == filter): 
                    filteredDataList.append(stockData)
        
        return filteredDataList

    def printStockData(self,stockData): 
        print(self.fullData)
        return 
            
        





    