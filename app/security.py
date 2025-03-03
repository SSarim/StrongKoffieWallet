import hashlib

def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def hash_address(address: str) -> str:
    return sha256_hash(address)