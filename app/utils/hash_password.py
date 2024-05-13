import hashlib

def hash_password(password : str) -> str:
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    return hashed_password


