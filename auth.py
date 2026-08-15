import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(user_name: str):
    payload = {
        "sub": user_name,
        "rol": "admin",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token_received: str):
    try:
        payload = jwt.decode(token_received, SECRET_KEY,
                             algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
