import sys 
import glob 
import os 
from datetime import date 
from ColorText import colorText
import configparser 

#TODO TEST MODULES
parser = configparser.ConfigParser(strict=False)

class config: 

    def __init__(self): 
        self.consolidationPercentage = 10
        self.volumeRatio = 2
        self.minLTP = 20.0
        self.maxLTP = 50000
        self.period = '300d'
        self.duration = '1d'
        self.daysToLookback = 30
        self.shuffleEnabled = True
        self.cacheEnabled = True
        self.stageTwo = False
        self.useEMA = False
        self.jfile = 'default.json'
    
    def setConfig(self,default=False,showFileCreatedText=True): 
        parser = configparser.ConfigParser(strict=False)
        if default: 
            parser.add_section('config')
            parser.set('config', 'period', self.period)
            parser.set('config', 'daysToLookback', str(self.daysToLookback))
            parser.set('config', 'duration', self.duration)
            parser.set('config', 'minPrice', str(self.minLTP))
            parser.set('config', 'maxPrice', str(self.maxLTP))
            parser.set('config', 'volumeRatio', str(self.volumeRatio))
            parser.set('config', 'consolidationPercentage',
                       str(self.consolidationPercentage))
            parser.set('config', 'shuffle', 'y')
            parser.set('config', 'cacheStockData', 'y')
            parser.set('config', 'onlyStageTwoStocks', 'y')
            parser.set('config', 'useEMA', 'n')
            parser.set('config', 'usefile', str(self.jfile))
            try: 
                fp = open('config.ini', 'w')
                parser.write(fp) 
                fp.close() 
                if showFileCreatedText: 
                    print(colorText.BOLD + colorText.GREEN +
                        '[+] Default configuration generated as user configuration is not found!' + colorText.END)
                    sys.exit(0)
            except IOError: 
                print(colorText.BOLD + colorText.FAIL +
                      '[+] Failed to save user config. Exiting..' + colorText.END)
                input('')
                sys.exit(1)
        else:
            parser.add_section('config') 
            print(colorText.BOLD + colorText.GREEN +
                  '[+] Enter The user Config:' + colorText.END)
            self.period = input(
                '[+] Enter number of days for which stock data to be downloaded (Days)(Optimal = 365): ')
            self.daysToLookback = input(
                '[+] Number of recent days (TimeFrame) to screen for Breakout/Consolidation (Days)(Optimal = 20): ')
            self.duration = input(
                '[+] Enter Duration of each candle (Days)(Optimal = 1): ')
            self.minLTP = input(
                '[+] Minimum Price of Stock to Buy (in RS)(Optimal = 20): ')
            self.maxLTP = input(
                '[+] Maximum Price of Stock to Buy (in RS)(Optimal = 50000): ')
            self.volumeRatio = input(
                '[+] How many times the volume should be more than average for the breakout? (Number)(Optimal = 2.5): ')
            self.consolidationPercentage = input(
                '[+] How many % the price should be in range to consider it as consolidation? (Number)(Optimal = 10): ')
            self.shuffle = str(input(
                '[+] Shuffle stocks rather than screening alphabetically? (Y/N): ')).lower()
            self.cacheStockData = str(input(
                '[+] Enable High-Performance and Data-Saver mode? (This uses little bit more CPU but performs High Performance Screening) (Y/N): ')).lower()
            self.stageTwoPrompt = str(input(
                '[+] Screen only for Stage-2 stocks?\n(What are the stages? => https://www.investopedia.com/articles/trading/08/stock-cycle-trend-price.asp)\n(Y/N): ')).lower()
            self.useEmaPrompt = str(input(
                '[+] Use EMA instead of SMA? (EMA is good for Short-term & SMA for Mid/Long-term trades)[Y/N]: ')).lower()
            parser.set('config', 'period', self.period + "d")
            parser.set('config', 'daysToLookback', self.daysToLookback)
            parser.set('config', 'duration', self.duration + "d")
            parser.set('config', 'minPrice', self.minLTP)
            parser.set('config', 'maxPrice', self.maxLTP)
            parser.set('config', 'volumeRatio', self.volumeRatio)
            parser.set('config', 'consolidationPercentage',
                       self.consolidationPercentage)
            parser.set('config', 'shuffle', self.shuffle)
            parser.set('config', 'cacheStockData', self.cacheStockData)
            parser.set('config', 'onlyStageTwoStocks', self.stageTwoPrompt)
            parser.set('config', 'useEMA', self.useEmaPrompt)

    #Check If config Exists
    def checkConfigFile(self):
        try:
            f = open('config.ini','r')
            f.close()
            return True
        except FileNotFoundError:
            return False
    
    def getConfig(self,parser):
        if len(parser.read('config.ini')):
                try:
                    self.duration = parser.get('config', 'duration')
                    self.period = parser.get('config', 'period')
                    self.minLTP = float(parser.get('config', 'minprice'))
                    self.maxLTP = float(parser.get('config', 'maxprice'))
                    self.volumeRatio = float(parser.get('config', 'volumeRatio'))
                    self.consolidationPercentage = float(
                        parser.get('config', 'consolidationPercentage'))
                    self.daysToLookback = int(
                        parser.get('config', 'daysToLookback'))
                    if 'n' not in str(parser.get('config', 'shuffle')).lower():
                        self.shuffleEnabled = True
                    if 'n' not in str(parser.get('config', 'cachestockdata')).lower():
                        self.cacheEnabled = True
                    if 'n' not in str(parser.get('config', 'onlyStageTwoStocks')).lower():
                        self.stageTwo = True
                    if 'y' not in str(parser.get('config', 'useEMA')).lower():
                        self.useEMA = False

                    self.jfile = parser.get('config', 'useFile').lower()
                    if(self.jfile == None): 
                        self.jfile = "default.json" 

                except configparser.NoOptionError:
                    input(colorText.BOLD + colorText.FAIL +
                        '[+] Screenipy requires user configuration again. Press enter to continue..' + colorText.END)
                    parser.remove_section('config')
                    self.setConfig(parser, default=False)
         
