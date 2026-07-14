import hashlib
import os

def hash_password(password: str)->str:
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt+password).encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(password:str, stored:str)->bool:
    salt, hashed = stored.split(":")
    return hashlib.sha256((salt+password).encode()).hexdigest() == hashed

