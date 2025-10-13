import os
import warnings
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Load configuration from environment with safe development defaults.
# In production, set a secure SECRET_KEY in the environment and avoid
# relying on defaults.
DEFAULT_SECRET = "dev-secret-please-change"
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET)
if SECRET_KEY == DEFAULT_SECRET:
    warnings.warn(
        "Using default SECRET_KEY. Set a secure SECRET_KEY in the environment for production.",
        UserWarning,
    )

ALGORITHM = os.getenv("ALGORITHM", "HS256")
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
except ValueError:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
