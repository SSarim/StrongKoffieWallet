import pytest
from app.models import TransactionModel
from pydantic import ValidationError

def test_valid_transaction_model():
    data = {"sender": "peer1", "receiver": "peer2", "amount": 10.5}
    tx = TransactionModel(**data)
    assert tx.sender == "peer1"
    assert tx.receiver == "peer2"
    assert tx.amount == 10.5

def test_invalid_transaction_model_amount():
    data = {"sender": "peer1", "receiver": "peer2", "amount": "invalid"}
    with pytest.raises(ValidationError):
        TransactionModel(**data)
