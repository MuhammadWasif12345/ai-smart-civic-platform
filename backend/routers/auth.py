from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from typing import List, Callable

from ..database import get_db
from ..models import User
from ..schemas import UserLogin, Token
from ..services.auth_service import AuthService

# --------------------------------------------------------------------------------
# AUTH ROUTER
# This file handles logging in and Role-Based Access Control (RBAC).
# --------------------------------------------------------------------------------

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency to get the currently logged-in user from the JWT token.
    """
    from jose import JWTError, jwt
    from ..services.auth_service import SECRET_KEY, ALGORITHM
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Your session expired or is invalid — please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
        
    return user

def require_role(allowed_roles: List[str]) -> Callable:
    """
    Dependency generator for RBAC. 
    Usage: dependencies=[Depends(require_role(["Super Admin", "Municipal Admin"]))]
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint for users to log in. They send username/password, we send back a token.
    """
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user or not AuthService.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
        
    # Include role and department in the JWT payload
    access_token = AuthService.create_access_token(
        data={
            "sub": user.username,
            "role": user.role,
            "department": user.department
        }
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role,
        "department": user.department
    }
