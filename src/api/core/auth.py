import hmac

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from hashlib import sha256


security = HTTPBearer()

def verify_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    SECRET_KEY = 'supersecretkey'
    ADMIN_CREDENTIALS = {'username': 'admin', 'password': 'test'}

    expected_token = hmac.new(
        SECRET_KEY.encode(),
        f"{ADMIN_CREDENTIALS['username']}:{ADMIN_CREDENTIALS['password']}".encode(),
        sha256
    ).hexdigest()
    
    if not hmac.compare_digest(token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True