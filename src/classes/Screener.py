import sys 
import math 
import numpy as np 
import pandas as pd  
import talib  
import datetime as dt
from ColorText import colorText
from candlePatterns import CandlePatterns


'''
Overlap Studies
BBANDS               Bollinger Bands
DEMA                 Double Exponential Moving Average
EMA                  Exponential Moving Average
HT_TRENDLINE         Hilbert Transform - Instantaneous Trendline
KAMA                 Kaufman Adaptive Moving Average
MA                   Moving average
MAMA                 MESA Adaptive Moving Average
MAVP                 Moving average with variable period
MIDPOINT             MidPoint over period
MIDPRICE             Midpoint Price over period
SAR                  Parabolic SAR
SAREXT               Parabolic SAR - Extended
SMA                  Simple Moving Average
T3                   Triple Exponential Moving Average (T3)
TEMA                 Triple Exponential Moving Average
TRIMA                Triangular Moving Average
WMA                  Weighted Moving Average

Momentum Indicators
ADX                  Average Directional Movement Index
ADXR                 Average Directional Movement Index Rating
APO                  Absolute Price Oscillator
AROON                Aroon
AROONOSC             Aroon Oscillator
BOP                  Balance Of Power
CCI                  Commodity Channel Index
CMO                  Chande Momentum Oscillator
DX                   Directional Movement Index
MACD                 Moving Average Convergence/Divergence
MACDEXT              MACD with controllable MA type
MACDFIX              Moving Average Convergence/Divergence Fix 12/26
MFI                  Money Flow Index
MINUS_DI             Minus Directional Indicator
MINUS_DM             Minus Directional Movement
MOM                  Momentum
PLUS_DI              Plus Directional Indicator
PLUS_DM              Plus Directional Movement
PPO                  Percentage Price Oscillator
ROC                  Rate of change : ((price/prevPrice)-1)*100
ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
ROCR                 Rate of change ratio: (price/prevPrice)
ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
RSI                  Relative Strength Index
STOCH                Stochastic
STOCHF               Stochastic Fast
STOCHRSI             Stochastic Relative Strength Index
TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
ULTOSC               Ultimate Oscillator
WILLR                Williams' %R

Volume Indicators
AD                   Chaikin A/D Line
ADOSC                Chaikin A/D Oscillator
OBV                  On Balance Volume

Cycle Indicators
HT_DCPERIOD          Hilbert Transform - Dominant Cycle Period
HT_DCPHASE           Hilbert Transform - Dominant Cycle Phase
HT_PHASOR            Hilbert Transform - Phasor Components
HT_SINE              Hilbert Transform - SineWave
HT_TRENDMODE         Hilbert Transform - Trend vs Cycle Mode

Price Transform
'''

class screener: 
    
    def __init__(self) -> None:
        pass
    
    # Private method to find candle type
    # True = Bullish, False = Bearish
    def getCandleType(self, stockData):
        return bool(stockData.trimmedData['Close'][0] >= stockData.trimmedData['Open'][0])
    

    def preprocessData(self,data,configManager ):
        if configManager.daysToLookback == None: 
            daysToLookback = configManager.daysToLookback
        else: 
            daysToLookback = 30

        if configManager.useEMA: 
            sma = talib.EMA(data['Close'], timeperiod = 50  ) 
            lma = talib.EMA(data['Close'],timeperiod = 200)  
        else: 
            sma = data.rolling(window = 50).mean() 
            lma = data.rolling(window = 200).mean() 
            
        data.insert(6,'SMA',sma['Close'])
        data.insert(7,'LMA',lma['Close'])
        vol = data.rolling(window=20).mean()
        rsi = talib.RSI(data['Close'], timeperiod=14)
        #bollingerBands 
        upBand,downBand,lowBand = talib.BBANDS(data['Close'], timeperiod= daysToLookback)
        data.insert(8,'VolMA',vol['Volume'])
        data.insert(9,'RSI',rsi)
        data.insert(10,'UPBAND',upBand)
        data.insert(11,'DOWNBAND',downBand) 
        data.insert(12,'LOWBAND',lowBand)
        data = data[::-1]               # Reverse the dataframe
        # data = data.fillna(0)
        # data = data.replace([np.inf, -np.inf], 0)
        fullData = data
        trimmedData = data.head(daysToLookback)
        return fullData, trimmedData
        

    def runScreener(self,data,screenerFunction,stockCode):
        #when passing function pass df to screener
        df = data 
        screenDataFrame = pd.DataFrame(screenerFunction(df,stockCode)) 


    def validateMovingAverages(self,stockData , maRange=2.5,):
        stockData.trimmedData = stockData.trimmedData.fillna(0)
        stockData.trimmedData = stockData.trimmedData.replace([np.inf, -np.inf], 0)
        recent = stockData.trimmedData.head(1)
        if(recent['SMA'][0] > recent['LMA'][0] and recent['Close'][0] > recent['SMA'][0]):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + 'Bullish' + colorText.END
            stockData.saveDict['MA-Signal'] = 'Bullish'
        elif(recent['SMA'][0] < recent['LMA'][0]):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + 'Bearish' + colorText.END
            stockData.saveDict['MA-Signal'] = 'Bearish'
        elif(recent['SMA'][0] == 0):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.WARN + 'Unknown' + colorText.END
            stockData.saveDict['MA-Signal'] = 'Unknown'
        else:
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.WARN + 'Neutral' + colorText.END
            stockData.saveDict['MA-Signal'] = 'Neutral'

        smaDev = stockData.trimmedData['SMA'][0] * maRange / 100
        lmaDev = stockData.trimmedData['LMA'][0] * maRange / 100
        open, high, low, close, sma, lma = stockData.trimmedData['Open'][0], stockData.trimmedData['High'][0], stockData.trimmedData['Low'][0], stockData.trimmedData['Close'][0], stockData.trimmedData['SMA'][0], stockData.trimmedData['LMA'][0]
        maReversal = 0
        # Taking Support 50
        if close > sma and low <= (sma + smaDev):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + '50MA-Support' + colorText.END
            stockData.saveDict['MA-Signal'] = '50MA-Support'
            maReversal = 1
        # Validating Resistance 50
        elif close < sma and high >= (sma - smaDev):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + '50MA-Resist' + colorText.END
            stockData.saveDict['MA-Signal'] = '50MA-Resist'
            maReversal = -1
        # Taking Support 200
        elif close > lma and low <= (lma + lmaDev):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + '200MA-Support' + colorText.END
            stockData.saveDict['MA-Signal'] = '200MA-Support'
            maReversal = 1
        # Validating Resistance 200
        elif close < lma and high >= (lma - lmaDev):
            stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + '200MA-Resist' + colorText.END
            stockData.saveDict['MA-Signal'] = '200MA-Resist'
            maReversal = -1
        # For a Bullish Candle
        if self.getCandleType(stockData.trimmedData):
            # Crossing up 50
            if open < sma and close > sma:
                stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + 'BullCross-50MA' + colorText.END
                stockData.saveDict['MA-Signal'] = 'BullCross-50MA'
                maReversal = 1            
            # Crossing up 200
            elif open < lma and close > lma:
                stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.GREEN + 'BullCross-200MA' + colorText.END
                stockData.saveDict['MA-Signal'] = 'BullCross-200MA'
                maReversal = 1
        # For a Bearish Candle
        elif not self.getCandleType(stockData.trimmedData):
            # Crossing down 50
            if open > sma and close < sma:
                stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + 'BearCross-50MA' + colorText.END
                stockData.saveDict['MA-Signal'] = 'BearCross-50MA'
                maReversal = -1         
            # Crossing up 200
            elif open > lma and close < lma:
                stockData.screenDict['MA-Signal'] = colorText.BOLD + colorText.FAIL + 'BearCross-200MA' + colorText.END
                stockData.saveDict['MA-Signal'] = 'BearCross-200MA'
                maReversal = -1
        return maReversal
    
    def validateVolume(self,stockData, volumeRatio=2.5):
        stockData.trimmedData = stockData.trimmedData.fillna(0)
        stockData.trimmedData = stockData.trimmedData.replace([np.inf, -np.inf], 0)
        recent = stockData.trimmedData.head(1)
        if recent['VolMA'][0] == 0: # Handles Divide by 0 warning
            stockData.saveDict['Volume'] = "Unknown"
            stockData.screenDict['Volume'] = colorText.BOLD + colorText.WARN + "Unknown" + colorText.END
            return True
        ratio = round(recent['Volume'][0]/recent['VolMA'][0],2)
        stockData.saveDict['Volume'] = str(ratio)+"x"
        if(ratio >= volumeRatio and ratio != np.nan and (not math.isinf(ratio)) and (ratio != 20)):
            stockData.screenDict['Volume'] = colorText.BOLD + colorText.GREEN + str(ratio) + "x" + colorText.END
            return True
        stockData.screenDict['Volume'] = colorText.BOLD + colorText.FAIL + str(ratio) + "x" + colorText.END
        return False

    

    def MarkMinevini(self,stockData): 
        '''
        Use original Data 
        The current stock price is above both the 150-day and 200-day moving average
        The 150-day moving average is above the 200-day moving average
        The 200-day moving average is trending up for at least 1 month
        The 50-day moving average is above both the 150-day and 200-day moving average
        The current stock price is trading above the 50-day moving average
        The current stock price is at least 30% above it’s 52-week low
        The current stock price is within at least 25% of it’s 52-week high
        The relative strength ranking (in IBD) is no less than 70, preferably in the 80’s or 90’s
        '''
        df = stockData.data.copy()
        df['SMA_200'] = df['Adj Close'].rolling(200).mean()
        df['SMA_150'] = df['Adj Close'].rolling(150).mean()
        df['SMA_50'] = df['Adj Close'].rolling(50).mean()
        
        # Determine the 52 week high and low
        low_of_52week=min(df["Adj Close"][-260:])
        high_of_52week=max(df["Adj Close"][-260:])

        # Storing required values 
        currentClose = df["Adj Close"][-1]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]
        low_of_52week = round(min(df["Low"][-260:]), 2)
        high_of_52week = round(max(df["High"][-260:]), 2)
        RSI = round(talib.RSI(df['Adj Close'] , timeperiod = 12),2) 

        try: 
            moving_average_200_20 = df["SMA_200"][-20]
        except Exception: 
            moving_average_200_20 = 0 
        #Condition 1: Current Price > 150 SMA and > 200 SMA
        condition_1 = currentClose > moving_average_150 > moving_average_200
        # Condition 2: 150 SMA and > 200 SMA
        condition_2 = moving_average_150 > moving_average_200
        # Condition 3: 200 SMA trending up for at least 1 month
        condition_3 = moving_average_200 > moving_average_200_20
        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        condition_4 = moving_average_50 > moving_average_150 > moving_average_200 
        # Condition 5: Current Price > 50 SMA
        condition_5 = currentClose > moving_average_50 
        # Condition 6: Current Price is at least 30% above 52 week low
        condition_6 = currentClose >= (1.3*low_of_52week) 
        # Condition 7: Current Price is within 25% of 52 week high
        condition_7 = currentClose >= (.75*high_of_52week)
        #conditon 8: RSI(maybe) > 70 
        condition_8 = RSI > 70.00
        condition = (condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7 and condition_8) 

        try:
            if condition == True: 
                stockData.screenDict["MarkMinerviTemplate"] = colorText.BOLD + colorText.GREEN + 'Yes' + colorText.END
                stockData.saveDict["MarkMinerviTemplate"] = "Yes"
            else: 
                stockData.screenDict["MarkMinerviTemplate"] = colorText.BOLD + colorText.FAIL + 'No' + colorText.END
                stockData.saveDict["MarkMinerviTemplate"] = "No"
        except:
            #print("Failed: ",stockData)
            stockData.screenDict["MarkMinerviTemplate"] = colorText.BOLD + colorText.FAIL + 'No' + colorText.END
            stockData.saveDict["MarkMinerviTemplate"] = "No"


    def screener1(self, stockData):
        if(stockData.fullData["Close"].rolling(window = 50).mean()  
           > stockData.fullData["Close"].rolling(window = 150).mean() and self.getCandleType(stockData.fullData)): 
            stockData.saveDict["Screener1"] = "Yes"
            return True


    def dictScreener(self): 
        screenerQueue = []
        #optionQueue = [] for multiple different types of screeners 
        print(colorText.BOLD + colorText.WARN + 
              """Enter your option
              [+] 1)> MarkMinveri Template 
              [+] 2)> Moving Averages 
              [+] 3)> Validate Volumes 
              [+] 4)> Candle Pattern 
              [+] 5)> All Patterns 
              """
             +colorText.END )
        screenerClass = screener()
        CandlePatternsClass = CandlePatterns()
        option = int(input(colorText.BOLD + colorText.WARN + "Enter option" + colorText.END ))
        screenerFunction = ({1: screenerClass.MarkMinevini , 2: screenerClass.validateVolume , 3: screenerClass.validateMovingAverages, 
                             4: CandlePatternsClass.findPattern , 5: screenerClass.screener1})
        
        try: 
            if option != 5: 
                screenerQueue.append(screenerFunction[option]) 
                return screenerQueue
            else: 
                screenerQueue = [screenerClass.MarkMinevini,screenerClass.validateVolume,
                                 screenerClass.validateMovingAverages,CandlePatternsClass.findPattern]
                return screenerQueue
        except KeyError:
            print(colorText.BOLD + colorText.FAIL + 'INVALID OPTION' + colorText.END)
            sys.exit(0) 
            

