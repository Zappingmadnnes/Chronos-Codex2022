# Just a file to toy around with API calls
from binance import Client
import pandas as pd 
from binance.enums import *
import json

client = Client("sRefEYbwTdAAcOTF79f31IC8PV40ReHw7WIkCxoEa1i0fneMDEwZJXfAfW9oYlvt", "DQ2BALot3rrrOJtcnpRB3tM65cN6ecm6wIxNe79FGJTwWT3jTBH7Qn1eun0mRztL", testnet=True)


# order = client.create_order(
#     symbol='ETHBTC',
#     side=SIDE_BUY,
#     type=ORDER_TYPE_LIMIT,
#     timeInForce=TIME_IN_FORCE_GTC,
#     quantity=1,
#     price='0.2')



balance = client.get_asset_balance(asset='ETH')
print(balance)

orders = client.get_all_orders(symbol='ETHBTC')
print(orders)
