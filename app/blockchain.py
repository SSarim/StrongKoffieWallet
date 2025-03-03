import hashlib
import json
from time import time
from app.security import hash_address

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = hash_address(sender)
        self.receiver = hash_address(receiver)
        self.amount = amount
        self.signature = signature  # Config  digital signature post test

    def to_dict(self):
        return self.__dict__

class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = time()
        self.transactions = transactions  # List of transaction dictionaries
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_data = {
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # def __repr__(self):
    #     return f"Block(Hash: {self.hash[:10]}..., previous_hash: {self.previous_hash[:10]}...)"

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # Initial funds by including a transaction in the genesis block
        initial_transactions = [
            {"sender": "NETWORK", "receiver": "peer1", "amount": 100},
            {"sender": "NETWORK", "receiver": "peer2", "amount": 100}
        ]
        genesis_block = Block(initial_transactions, "0")
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Transaction):
        new_block = Block([transaction.to_dict()], self.chain[-1].hash)
        self.chain.append(new_block)
        return new_block
        # validate digital signatures and other details

        # self.pending_transactions.append(transaction.to_dict())

    def get_balance(self, address: str):
        balance = 0
        hashed_address = hash_address(address)
        for block in self.chain:
            for tx in block.transactions:
                if tx["sender"] == address:
                    balance -= tx["amount"]
                if tx["receiver"] == address:
                    balance += tx["amount"]
        # Also include pending transactions
        # for tx in self.pending_transactions:
        #     if tx["sender"] == address:
        #         balance -= tx["amount"]
        #     if tx["receiver"] == address:
        #         balance += tx["amount"]
        return balance

    def get_transaction_history(self):
        history = []
        for block in self.chain:
            history.extend(block.transactions)
        #  include pending transactions
        return history
