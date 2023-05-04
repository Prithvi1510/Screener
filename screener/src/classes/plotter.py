import yfinance as yf
import plotly.graph_objects as go
import plotly
import numpy as np 
import matplotlib.pyplot as plt 
# data = yf.download(tickers = "TATASTEEL.NS" , period= '1d' , interval = '30m')

# fig = go.Figure(data=[go.Candlestick(x=data.index,
#                                      open=data['Open'],
#                                      high=data['High'],
#                                      low=data['Low'],
#                                      close=data['Close'])])

# fig.show() 
# fig


class Plotter(): 
    
    def __init__(self): 
        pass    

    
    def show(self,stockdata,trimmed= True):
        fig,ax =  plt.subplots(2,2)

        if(trimmed == True):
            data = stockdata.trimmedData
        else: 
            data = stockdata.fullData

        #plot 1 Closing Data 
        ax[0,0].plot(data["Close"])
        ax[0,0].title.set_text("Closing Data")
        ax[0,0].set_xlabel("Date")
        ax[0,0].set_ylabel("stock Price") 
        ax[0,0].grid()

        #plot 2 Bollinger Bands 
        ax[0,1].plot(data["UPBAND"])
        ax[0,1].plot(data["DOWNBAND"])
        ax[0,1].plot(data["LOWBAND"])
        ax[0,1].plot(data["Close"])
        ax[0,1].set_xlabel("Date") 
        ax[0,1].set_ylabel("Bands")
        ax[0,1].grid()

        

        #Plot 3 RSI
        ax[1,0].plot(data['RSI'])
        ax[1,0].title.set_text("RSI")
        ax[1,0].set_xlabel("Date") 
        ax[1,0].set_ylabel("RSI") 
        ax[1,0].grid()


        return fig
        




        

    
