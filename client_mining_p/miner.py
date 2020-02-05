import hashlib
import requests

import sys
import json


def proof_of_work(block):
    print('Running proof of work')
    proof = 0
    string_obj = json.dumps(block)
    while valid_proof(string_obj, proof) == False:
        proof += 1

    print('Proof found')
    return proof


def valid_proof(block_string, proof):
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == '000000'

coins_mined = 0

if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # Get the block from `data` and use it to look for a new proof
        new_proof = proof_of_work(data)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if data['message'] == 'New Block Forged':
            coins_mined += 1
            print(f'Coins Mined: {coins_mined}')
        else:
            print('Server message: ', data['message'])
