import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        # Create the block_string from a stringified json block that is then encoded
        block_string = json.dumps(block).encode()
        # Hash this string using sha256, and change to hexadecimal form
        hash_string = hashlib.sha256(block_string).hexdigest()

        return hash_string

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        proof = 0
        string_obj = json.dumps(block, sort_keys=False)
        while self.valid_proof(string_obj, proof) == False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(block_string, proof):
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:3] == '000'



# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    proof = blockchain.proof_of_work(blockchain.last_block)
    prev_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.new_block(proof, prev_hash)
    response = {
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
