from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from ..database import get_db
from ..models import Admin
from ..schemas import AdminLogin, Token
from ..services.auth_service import AuthService

# --------------------------------------------------------------------------------
# AUTH ROUTER
# This file handles logging in to the admin dashboard.
# --------------------------------------------------------------------------------

router = APIRouter()

# This is a FastAPI built-in that extracts the JWT token from the Authorization header
# of incoming requests. Any endpoint that depends on this will require the user to be logged in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This is a "Dependency". We attach this to admin routes to automatically
    check if the person calling the API is a logged-in admin.
    """
    from jose import JWTError, jwt
    from ..services.auth_service import SECRET_KEY, ALGORITHM
    
    # Generic error to throw if something is wrong with the token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Your session expired or is invalid — please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Try to read and verify the token using our secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        # If the token is fake or expired, throw the error
        raise credentials_exception
        
    # Check if the user still actually exists in our database
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None:
        raise credentials_exception
        
    return admin


@router.post("/login", response_model=Token)
def login(admin_data: AdminLogin, db: Session = Depends(get_db)):
    """
    Endpoint for admins to log in. They send username/password, we send back a token.
    """
    # 1. Look up the admin in the database by their username
    admin = db.query(Admin).filter(Admin.username == admin_data.username).first()
    
    # 2. Check if the admin exists AND if the password they typed matches the hash in the DB
    if not admin or not AuthService.verify_password(admin_data.password, admin.hashed_password):
        # We throw a 401 Unauthorized error. 
        # Notice we say "Incorrect username or password" rather than "User not found".
        # This is a security best practice so hackers can't guess valid usernames.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
        
    # 3. The password was correct! Generate a new JWT token for them.
    # The "sub" (subject) field conventionally holds the username.
    access_token = AuthService.create_access_token(data={"sub": admin.username})
    
    return {"access_token": access_token, "token_type": "bearer"}
