import os
import sys
from web3 import Web3

# 1. Fetch seed phrase / key safely from GitHub Secrets
PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")

if not PRIVATE_KEY:
    print("Error: WALLET_PRIVATE_KEY secret is missing!")
    sys.exit(1)

# 2. Connect to Optimism Sepolia Testnet RPC
RPC_URL = "https://sepolia.optimism.io"
w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    print("Failed to connect to the Web3 network.")
    sys.exit(1)

# 3. Derive wallet address from key/mnemonic
try:
    if len(PRIVATE_KEY.split()) >= 12:
        w3.eth.account.enable_unaudited_hdwallet_features()
        account = w3.eth.account.from_mnemonic(PRIVATE_KEY)
    else:
        account = w3.eth.account.from_key(PRIVATE_KEY)
except Exception as e:
    print(f"Error initializing account: {e}")
    sys.exit(1)

address = account.address
print(f"Successfully connected! Wallet Address: {address}")

# 4. Check testnet ETH balance
balance_wei = w3.eth.get_balance(address)
balance_eth = w3.from_wei(balance_wei, 'ether')

print(f"Current Optimism Sepolia Balance: {balance_eth} ETH")
print("Task completed successfully!")
