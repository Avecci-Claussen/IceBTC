import time
import multiprocessing
import secp256k1
from secp256k1 import get_sha256


def mine_batch(block_number, transactions, previous_hash, prefix_zeros, nonce_range, btc_address):
    prefix_str = '0' * prefix_zeros
    base_text = f"{block_number}{transactions}{previous_hash}Reward to {btc_address}"

    for nonce in range(*nonce_range):
        text = f"{base_text}{nonce}"
        new_hash = get_sha256(text)
        #print(f"Trying nonce {nonce}: {new_hash}")
        if new_hash.startswith(prefix_str.encode()):
            return nonce, new_hash.hex()

    return None, None

def mine_parallel(block_number, transactions, previous_hash, prefix_zeros, start_nonce, end_nonce, btc_address, num_processes=10):
    # Divide the range into batches
    batch_size = (end_nonce - start_nonce) // num_processes
    nonce_ranges = [(start_nonce + i * batch_size, min(start_nonce + (i + 1) * batch_size, end_nonce)) for i in range(num_processes)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(mine_batch, [(block_number, transactions, previous_hash, prefix_zeros, nonce_range, btc_address) for nonce_range in nonce_ranges])

    # Check results
    for nonce, hash_hex in results:
        if nonce is not None:
            return nonce, hash_hex

    raise BaseException("Couldn't find correct hash in nonce range")
    
    
def main():
    block_number = 816333
    transactions = '3e0b8259259140b1f32b78d4c323b5ec278e6be80ba9ebf92e5ea8354eae5260'
    previous_hash = '00000000000000000000ef01152c31f4322b500926ad4590e612998260d6c16a'
    prefix_zeros = 20  # High difficulty level
    btc_address = '39aHPRr3eyoHWyTeKwtyS86y7wXc71FPk9'
    start_nonce = 2444100037
    end_nonce = 2454100037  # Adjust this range as needed

    start = time.time()
    try:
        nonce, new_hash = mine_parallel(block_number, transactions, previous_hash, prefix_zeros, start_nonce, end_nonce, btc_address)
        total_time = str(time.time() - start)
        print(f"Bitcoin mined with nonce value: {nonce}")
        print(f"Mining took: {total_time} seconds")
        print(new_hash)
    except BaseException as e:
        print(e)

if __name__ == '__main__':
    main()
    
