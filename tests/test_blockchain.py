import pytest
from app.blockchain import Blockchain, Transaction
from app.security import hash_address

def test_genesis_block_creation():
    blockchain = Blockchain()
    # The genesis block should already be created.
    assert len(blockchain.chain) == 1
    genesis_block = blockchain.chain[0]
    transactions = genesis_block.transactions
    # Check that one of the transactions gives 100 to peer1.
    receivers = [tx["receiver"] for tx in transactions]
    amounts = [tx["amount"] for tx in transactions]
    assert hash_address("peer1") in receivers
    assert 100 in amounts

def test_add_transaction_and_balance():
    blockchain = Blockchain()
    initial_balance = blockchain.get_balance("peer1")
    tx = Transaction("peer1", "peer2", 50)
    blockchain.add_transaction(tx)
    new_balance = blockchain.get_balance("peer1")
    assert new_balance == initial_balance - 50

def test_transaction_history():
    blockchain = Blockchain()
    tx1 = Transaction("peer1", "peer2", 20)
    tx2 = Transaction("peer2", "peer1", 10)
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    history = blockchain.get_transaction_history()
    # Genesis block has two transactions; then one block per added transaction.
    expected_count = len(blockchain.chain[0].transactions) + 2
    assert len(history) == expected_count
