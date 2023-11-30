import time
import hashlib
import requests
import secp256k1
from secp256k1 import get_sha256

def get_latest_block_info():
    print("Fetching latest block info...")
    try:
        response = requests.get("https://blockchain.info/latestblock")
        latest_block = response.json()

        block_number = latest_block['height']
        previous_hash = latest_block['hash']

        response = requests.get(f"https://blockchain.info/rawblock/{previous_hash}")
        block_data = response.json()
        transactions = block_data['tx'][0]['hash']

        # Fetch current difficulty
        difficulty_response = requests.get("https://blockchain.info/q/getdifficulty")
        difficulty = difficulty_response.json()

        return block_number, transactions, previous_hash, difficulty
    except Exception as e:
        print(f"Error fetching block info: {e}")
        raise
        
def mine(block_number, transactions, previous_hash, prefix_zeros, start_nonce, end_nonce, btc_address):
    prefix_str = '0' * prefix_zeros
    reward_transaction = f"Reward to {btc_address}"
    transactions += reward_transaction

    for nonce in range(start_nonce, end_nonce):
        if nonce % 1000000 == 0:
            print(f"Checked {nonce - start_nonce} hashes so far...")
        text = str(block_number) + transactions + previous_hash + str(nonce)
        new_hash = hashlib.sha256(text.encode('ascii')).hexdigest()

        #print(f"Trying nonce {nonce}: {new_hash}")

        if new_hash.startswith(prefix_str):
            print(f"Bitcoin mined with nonce value: {nonce}")
            return new_hash

    raise BaseException(f"Couldn't find correct hash in nonce range {start_nonce}-{end_nonce}")

block_number, transactions, previous_hash = get_latest_block_info()
prefix_zeros = 20  # Assuming a fixed difficulty level for simplicity
btc_address = '39aHPRr3eyoHWyTeKwtyS86y7wXc71FPk9'
start_nonce = 2444100037
end_nonce = 4444100037

start = time.time()
    try:
        block_number, transactions, previous_hash, difficulty = get_latest_block_info()
        print(f"Block Number: {block_number}, Transactions: {transactions}, Previous Hash: {previous_hash}, Difficulty: {difficulty}")
        
        # Convert difficulty to prefix_zeros (simplified, see note below)
        prefix_zeros = int(difficulty / 100000000000) # This is a simplification. Real calculation might differ.
        btc_address = '39aHPRr3eyoHWyTeKwtyS86y7wXc71FPk9'
        start_nonce = 2444100037
        end_nonce = 4444100037

        start = time.time()
        new_hash = mine(block_number, transactions, previous_hash, prefix_zeros, start_nonce, end_nonce, btc_address)
        total_time = str(time.time() - start)
        print(f"Mining Block Number: {block_number}")
        print(f"Bitcoin mined with nonce value: {nonce}")
        print(f"Mining took: {total_time} seconds")
        print(new_hash)
    except Exception as e:
        print(f"An error occurred: {e}")
