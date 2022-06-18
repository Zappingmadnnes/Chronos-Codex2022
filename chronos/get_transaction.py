import json

from hexbytes import HexBytes
from web3 import Web3

# 2. Set web3 module
infura_url = "https://mainnet.infura.io/v3/54b20ff0973a47b78c95d762da99982b"
web3 = Web3(Web3.HTTPProvider(infura_url))

# 3. Print Connection check
print(web3.isConnected())

# 4. Get Block Number
print(web3.eth.blockNumber)

#print(web3.eth.get_block(14980535))

class HexJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return super().default(obj)

tx = web3.eth.get_block('pending')
tx_dict = dict(tx)
#print(tx_dict.transactions)


for i in tx_dict ['transactions']:
    #print(i.hex())
    txs = web3.eth.get_transaction(i.hex())
    txs_dict = dict(txs)
    print(txs_dict.blockNumber)

f.close()
#tx_json = json.dumps(tx_dict, cls=HexJsonEncoder)


#f = open("output.json", "w")
#f.write(tx_json)
#f.close()