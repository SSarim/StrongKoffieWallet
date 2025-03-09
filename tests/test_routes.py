import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routes import router, blockchain
from app.auth import get_current_user


from starlette.middleware.base import BaseHTTPMiddleware
# Set the session in request.scope. for the middleware.
class DummySessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if "session" not in request.scope:
            request.scope["session"] = {}
        response = await call_next(request)
        return response

# Override dependency to test authenticated user "peer1".
def override_get_current_user():
    return {"username": "peer1"}

app = FastAPI()
app.add_middleware(DummySessionMiddleware)
app.include_router(router)
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_blockchain():
    # Reset the blockchain state before each test.
    blockchain.chain = []
    blockchain.create_transaction_block()
    yield

def test_get_balance():
    response = client.get("/balance/")
    assert response.status_code == 200
    data = response.json()
    # Network transaction block gives peer1 an initial balance of 100.
    assert data["address"] == "peer1"
    assert data["balance"] == 100

def test_get_transaction_history():
    response = client.get("/transactions/")
    assert response.status_code == 200
    data = response.json()
    # Network transaction block should include 2 transactions.
    assert "transactions" in data
    assert len(data["transactions"]) == 2

def test_create_transaction_success():
    # Valid transaction: peer1 sends 50 to peer2.
    payload = {"sender": "peer1", "receiver": "peer2", "amount": 50}
    response = client.post("/transaction/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Transaction recorded" in data["message"]

    # Verify that peer1's balance is updated.
    balance_response = client.get("/balance/")
    balance_data = balance_response.json()
    assert balance_data["balance"] == 50

def test_create_transaction_insufficient_funds():
    # Send an amount greater than the balance.
    payload = {"sender": "peer1", "receiver": "peer2", "amount": 150}
    response = client.post("/transaction/", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Insufficient funds"

def test_create_transaction_unauthorized():
    # Sender does not match the authenticated user for a transaction.
    payload = {"sender": "another", "receiver": "peer2", "amount": 10}
    response = client.post("/transaction/", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Unauthorized: You can only send from your own account!"
