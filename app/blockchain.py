# import hashlib
# import json
# from time import time
#
# from sqlalchemy.sql.functions import user
#
# from app.security import hash_address
#
# class Transaction:
#     def __init__(self, sender, receiver, amount, signature=None):
#         # Convert addresses to hashed versions
#         self.sender = hash_address(sender)
#         self.receiver = hash_address(receiver)
#         self.amount = amount
#         self.signature = signature  # Placeholder for future digital signatures
#
#     def to_dict(self):
#         return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount, "signature": self.signature}
#
# class Block:
#     def __init__(self, transactions, previous_hash):
#         self.timestamp = time()
#         self.transactions = transactions  # List of transaction dictionaries
#         self.previous_hash = previous_hash
#         self.hash = self.compute_hash()
#
#     def compute_hash(self):
#         block_data = {
#             "timestamp": self.timestamp,
#             "transactions": self.transactions,
#             "previous_hash": self.previous_hash,
#         }
#         block_string = json.dumps(block_data, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()
#
# class Blockchain:
#     def __init__(self):
#         self.chain = []
#         self.create_transaction_block()
#
#     def create_transaction_block(self):
#         # Preload initial funds using hashed addresses for consistency.
#         initial_transactions = [
#             # {"sender": "NETWORK", "receiver": hash_address(user.username), "amount": 100},
#             {"sender": "NETWORK", "receiver": hash_address("peer1"), "amount": 100},
#             {"sender": "NETWORK", "receiver": hash_address("peer2"), "amount": 100}
#         ]
#         transaction_block = Block(initial_transactions, "0")
#         self.chain.append(transaction_block)
#
#     def add_transaction(self, transaction: Transaction):
#         new_block = Block([transaction.to_dict()], self.chain[-1].hash)
#         self.chain.append(new_block)
#         return new_block
#
#     def get_balance(self, address: str):
#         balance = 0
#         hashed_address = hash_address(address)
#         for block in self.chain:
#             for tx in block.transactions:
#                 if tx["sender"] == hashed_address:
#                     balance -= tx["amount"]
#                 if tx["receiver"] == hashed_address:
#                     balance += tx["amount"]
#         return balance
#
#     def get_transaction_history(self):
#         history = []
#         for block in self.chain:
#             history.extend(block.transactions)
#         return history
#
# # Token Login system as a fallback if program does not work
# """
# class Transaction:
#     def __init__(self, sender, receiver, amount, signature=None):
#         # Hash the addresses so that only hashed identifiers are stored.
#         self.sender = hash_address(sender)
#         self.receiver = hash_address(receiver)
#         self.amount = amount
#         self.signature = signature
#
#     def to_dict(self):
#         return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount, "signature": self.signature}
#
# class Block:
#     def __init__(self, transactions, previous_hash):
#         self.timestamp = time()
#         self.transactions = transactions  # List of transaction dictionaries
#         self.previous_hash = previous_hash
#         self.hash = self.compute_hash()
#
#     def compute_hash(self):
#         block_data = {
#             "timestamp": self.timestamp,
#             "transactions": self.transactions,
#             "previous_hash": self.previous_hash,
#         }
#         block_string = json.dumps(block_data, sort_keys=True).encode()
#         return hashlib.sha256(block_string).hexdigest()
#
# class Blockchain:
#     def __init__(self):
#         self.chain = []
#         self.create_transaction_block()
#
#     def create_transaction_block(self):
#         #  initial funds with hashed addresses
#         initial_transactions = [
#             {"sender": "NETWORK", "receiver": hash_address("peer1"), "amount": 100},
#             {"sender": "NETWORK", "receiver": hash_address("peer2"), "amount": 100}
#         ]
#         transaction_block = Block(initial_transactions, "0")
#         self.chain.append(transaction_block)
#
#     def add_transaction(self, transaction: Transaction):
#         new_block = Block([transaction.to_dict()], self.chain[-1].hash)
#         self.chain.append(new_block)
#         return new_block
#
#     def get_balance(self, address: str):
#         balance = 0
#         hashed_address = hash_address(address)
#         for block in self.chain:
#             for tx in block.transactions:
#                 if tx["sender"] == hashed_address:
#                     balance -= tx["amount"]
#                 if tx["receiver"] == hashed_address:
#                     balance += tx["amount"]
#         return balance
#
#     def get_transaction_history(self):
#         history = []
#         for block in self.chain:
#             history.extend(block.transactions)
#         return history
# """