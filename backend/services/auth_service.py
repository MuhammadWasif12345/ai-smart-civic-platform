from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

# --------------------------------------------------------------------------------
# AUTH SERVICE
# Handles the security for the admin dashboard: password hashing and JWT token generation.
# --------------------------------------------------------------------------------

# We grab the secret key used to sign our tokens from the .env file.
# If someone gets this key, they can forge admin tokens, so it must be kept secret.
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_for_dev_only_123")
ALGORITHM = "HS256"
# Tokens expire after 60 minutes for security
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# We set up passlib to use the bcrypt algorithm. Bcrypt is a standard, highly secure
# way to scramble (hash) passwords so that even if the database is stolen, the 
# passwords can't be read.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class AuthService:
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        # We can't un-hash a password to check it. Instead, we hash the plain password
        # the user just typed in, and see if it matches the hash we have in the database.
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        # Takes a plain text password and returns the scrambled bcrypt version
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        # We make a copy of the data (usually just {"sub": username}) so we don't alter the original
        to_encode = data.copy()
        
        # Figure out when this token should expire
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        # Add the expiration time to the token's payload under the standard "exp" key
        to_encode.update({"exp": expire})
        
        # Cryptographically sign the token using our secret key. 
        # This proves the token was issued by us and hasn't been tampered with.
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
