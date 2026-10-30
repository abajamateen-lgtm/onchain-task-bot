import os
import sys
from web3 import Web3

# Fetch seed phrase safely from GitHub Secrets
PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")

if not PRIVATE_KEY:
    print("Error: WALLET_PRIVATE_KEY secret is missing!")
    sys.exit(1)

# List of major testnets to monitor
NETWORKS = [
    {"name": "Optimism Sepolia", "rpc": "https://sepolia.optimism.io"},
    {"name": "Arbitrum Sepolia", "rpc": "https://sepolia-rollup.arbitrum.io/rpc"},
    {"name": "Base Sepolia", "rpc": "https://sepolia.base.org"},
    {"name": "Polygon Amoy", "rpc": "https://rpc-amoy.polygon.technology"}
]

print("--- STARTING MULTI-NETWORK BALANCE CHECK ---")

for net in NETWORKS:
    try:
        w3 = Web3(Web3.HTTPProvider(net["rpc"]))
        if not w3.is_connected():
            print(f"[{net['name']}] Connection failed.")
            continue

        # Derive account from 12-word seed or private key
        if len(PRIVATE_KEY.split()) >= 12:
            w3.eth.account.enable_unaudited_hdwallet_features()
            account = w3.eth.account.from_mnemonic(PRIVATE_KEY)
        else:
            account = w3.eth.account.from_key(PRIVATE_KEY)

        address = account.address
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')

        print(f"[{net['name']}] Wallet: {address} | Balance: {balance_eth}")
    except Exception as e:
        print(f"[{net['name']}] Error checking network: {e}")

print("--- MULTI-NETWORK TASK COMPLETED ---")
