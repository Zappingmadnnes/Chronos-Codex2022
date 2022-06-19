from binance.client import Client
from binance import ThreadedWebsocketManager
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time


class statistical_arbitrage_bot():
    def __init__(self, symbol, bar_length):
        print("Init")

        self.symbol = symbol
        self.bar_length = bar_length


    def start_trading(self, historical_days):
        print("Starting trading")

        self.twm = ThreadedWebsocketManager()
        self.twm.start()

        self.get_most_recent(symbol = self.symbol, interval = self.bar_length,
                                 days = historical_days)

        self.twm.start_kline_socket(callback = self.stream_candles,
                                        symbol = self.symbol, interval = self.bar_length)



    def get_most_recent(self, symbol, interval, days):
        print("get_most_recent")
    
        now = datetime.utcnow()
        past = str(now - timedelta(days = days))

        print("1")
    
        bars = client.get_historical_klines(symbol = symbol, interval = interval,
                                            start_str = past, end_str = None, limit = 1000)
        df = pd.DataFrame(bars)
        df["Date"] = pd.to_datetime(df.iloc[:,0], unit = "ms")
        df.columns = ["Open Time", "Open", "High", "Low", "Close", "Volume",
                      "Clos Time", "Quote Asset Volume", "Number of Trades",
                      "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore", "Date"]
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()
        df.set_index("Date", inplace = True)
        print("2")
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors = "coerce")
        df["Complete"] = [True for row in range(len(df)-1)] + [False]
        print("3")
        self.data = df
        print(df)
    
    def stream_candles(self, msg):
        print("Streaming candles")
        
        # extract the required items from msg
        event_time = pd.to_datetime(msg["E"], unit = "ms")
        start_time = pd.to_datetime(msg["k"]["t"], unit = "ms")
        first   = float(msg["k"]["o"])
        high    = float(msg["k"]["h"])
        low     = float(msg["k"]["l"])
        close   = float(msg["k"]["c"])
        volume  = float(msg["k"]["v"])
        complete=       msg["k"]["x"]
        
        # # stop trading session
        # if self.trades >= 5: # stop stream after 5 trades
        #     self.twm.stop()
        #     if self.position == 1:
        #         order = client.create_order(symbol = self.symbol, side = "SELL", type = "MARKET", quantity = self.units)
        #         self.report_trade(order, "GOING NEUTRAL AND STOP")
        #         self.position = 0
        #     elif self.position == -1:
        #         order = client.create_order(symbol = self.symbol, side = "BUY", type = "MARKET", quantity = self.units)
        #         self.report_trade(order, "GOING NEUTRAL AND STOP")
        #         self.position = 0
        #     else: 
        #         print("STOP")
    
        # print out
        print(".", end = "", flush = True) # just print something to get a feedback (everything OK) 
    
        # feed df (add new bar / update latest bar)
        self.data.loc[start_time] = [first, high, low, close, volume, complete]
        
        # prepare features and define strategy/trading positions whenever the latest bar is complete
        if complete == True:
            self.define_strategy()
            self.execute_trade()

    def define_strategy(self):
        print("Defining strategy")

        df = self.data.copy()
    def execute_trade(self):
        print("Executing trade")


if __name__ == "__main__":

    #Test net keys
    api_key = "08EXjdKMKAHFhhWZCBEopVCwIwBI5SlBjPvGJaoSa0TGJOfkO8COtyPVH6RIMvwI"
    secret_key = "f0fGWOEfOKdIxw6tbzlUF8WyXj3CS7wEJMrq8MK9KlsrdovZ6iIS9Z5ZysQ1uCaa"

    client = Client(api_key = api_key, api_secret = secret_key, tld = "com", testnet = True)

    symbol = "ETHUSDT"
    bar_length = "1m"

    trader = statistical_arbitrage_bot(symbol = symbol, bar_length = bar_length)

    trader.start_trading(historical_days = 1/24)