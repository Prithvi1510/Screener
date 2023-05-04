import json 
import pandas as pd 
import os


'''
{ 
    "index" : false,
    "indexused" : "notused",
    "stockcodes" : ["ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "HDFC", "ICICIBANK", "ITC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", "SBILIFE", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"]},
}
'''

class jsonConfig(): 
    
    def __init__(self,defaultConfig):
        path = os.path.join(os.getcwd(),'configJSON',defaultConfig.jfile)
        try:  
            with open(path, 'r') as json_file: 
                jsonDicitionary = json.load(json_file) 
        except Exception as e: 
            print(e)
        
        self.index = jsonDicitionary["index"]
        self.indexUsed = jsonDicitionary["indexused"]
        self.stockcodes = jsonDicitionary["stockcodes"]
        
        # if self.index == True and self.indexUsed != "notused": 
        #     self.stockcodes ==  []

        