import pandas as pd
import talib
from ColorText import colorText


class CandlePatterns:

    reversalPatternsBullish = ['Morning Star', 'Morning Doji Star', '3 Inside Up', 'Hammer', '3 White Soldiers', 'Bullish Engulfing', 'Dragonfly Doji', 'Supply Drought', 'Demand Rise']
    reversalPatternsBearish = ['Evening Star', 'Evening Doji Star', '3 Inside Down', 'Inverted Hammer', 'Hanging Man', '3 Black Crows', 'Bearish Engulfing', 'Shooting Star', 'Gravestone Doji']

    def __init__(self):
        pass

    # Find candle-stick patterns
    # Arrange if statements with max priority from top to bottom
    def findPattern(self, stockData,):
        data = stockData.trimmedData.head(4)
        data = data[::-1]

        check = talib.CDLMORNINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Morning Star' + colorText.END
            stockData.saveDict['Pattern'] = 'Morning Star'
            return True

        check = talib.CDLMORNINGDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Morning Doji Star' + colorText.END
            stockData.saveDict['Pattern'] = 'Morning Doji Star'
            return True
        
        check = talib.CDLEVENINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Evening Star' + colorText.END
            stockData.saveDict['Pattern'] = 'Evening Star'
            return True

        check = talib.CDLEVENINGDOJISTAR(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Evening Doji Star' + colorText.END
            stockData.saveDict['Pattern'] = 'Evening Doji Star'
            return True

        check = talib.CDLLADDERBOTTOM(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Ladder Bottom' + colorText.END
                stockData.saveDict['Pattern'] = 'Bullish Ladder Bottom'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Ladder Bottom' + colorText.END
                stockData.saveDict['Pattern'] = 'Bearish Ladder Bottom'
            return True

        check = talib.CDL3LINESTRIKE(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + '3 Line Strike' + colorText.END
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + '3 Line Strike' + colorText.END
            stockData.saveDict['Pattern'] = '3 Line Strike'
            return True
        
        check = talib.CDL3BLACKCROWS(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + '3 Black Crows' + colorText.END
            stockData.saveDict['Pattern'] = '3 Black Crows'
            return True

        check = talib.CDL3INSIDE(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + '3 Outside Up' + colorText.END
                stockData.saveDict['Pattern'] = '3 Inside Up'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + '3 Outside Down' + colorText.END
                stockData.saveDict['Pattern'] = '3 Inside Down'
            return True

        check = talib.CDL3OUTSIDE(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + '3 Outside Up' + colorText.END
                stockData.saveDict['Pattern'] = '3 Outside Up'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + '3 Outside Down' + colorText.END
                stockData.saveDict['Pattern'] = '3 Outside Down'
            return True

        check = talib.CDL3WHITESOLDIERS(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + '3 White Soldiers' + colorText.END
            stockData.saveDict['Pattern'] = '3 White Soldiers'
            return True

        check = talib.CDLHARAMI(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Bullish Harami' + colorText.END
                stockData.saveDict['Pattern'] = 'Bullish Harami'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Bearish Harami' + colorText.END
                stockData.saveDict['Pattern'] = 'Bearish Harami'
            return True

        check = talib.CDLHARAMICROSS(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Bullish Harami Cross' + colorText.END
                stockData.saveDict['Pattern'] = 'Bullish Harami Cross'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Bearish Harami Cross' + colorText.END
                stockData.saveDict['Pattern'] = 'Bearish Harami Cross'
            return True

        check = talib.CDLMARUBOZU(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Bullish Marubozu' + colorText.END
                stockData.saveDict['Pattern'] = 'Bullish Marubozu'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Bearish Marubozu' + colorText.END
                stockData.saveDict['Pattern'] = 'Bearish Marubozu'
            return True

        check = talib.CDLHANGINGMAN(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Hanging Man' + colorText.END
            stockData.saveDict['Pattern'] = 'Hanging Man'
            return True
        
        check = talib.CDLHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Hammer' + colorText.END
            stockData.saveDict['Pattern'] = 'Hammer'
            return True

        check = talib.CDLINVERTEDHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Inverted Hammer' + colorText.END
            stockData.saveDict['Pattern'] = 'Inverted Hammer'
            return True

        check = talib.CDLSHOOTINGSTAR(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Shooting Star' + colorText.END
            stockData.saveDict['Pattern'] = 'Shooting Star'
            return True

        check = talib.CDLDRAGONFLYDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Dragonfly Doji' + colorText.END
            stockData.saveDict['Pattern'] = 'Dragonfly Doji'
            return True

        check = talib.CDLGRAVESTONEDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Gravestone Doji' + colorText.END
            stockData.saveDict['Pattern'] = 'Gravestone Doji'
            return True

        check = talib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            stockData.screenDict['Pattern'] = colorText.BOLD + 'Doji' + colorText.END
            stockData.saveDict['Pattern'] = 'Doji'
            return True

        check = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
        if(check.tail(1).item() != 0):
            if(check.tail(1).item() > 0):
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.GREEN + 'Bullish Engulfing' + colorText.END
                stockData.saveDict['Pattern'] = 'Bullish Engulfing'
            else:
                stockData.screenDict['Pattern'] = colorText.BOLD + colorText.FAIL + 'Bearish Engulfing' + colorText.END
                stockData.saveDict['Pattern'] = 'Bearish Engulfing'
            return True

        stockData.screenDict['Pattern'] = ''
        stockData.saveDict['Pattern'] = ''
        return False
