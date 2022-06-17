
from web3 import Web3

# 2. Set web3 module
infura_url = "https://mainnet.infura.io/v3/54b20ff0973a47b78c95d762da99982b"
web3 = Web3(Web3.HTTPProvider(infura_url))

# 3. Print Connection check
print(web3.isConnected())

# 4. Get Block Number
print(web3.eth.blockNumber)

print(web3.eth.get_block(2000000))