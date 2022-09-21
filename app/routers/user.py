from fastapi import APIRouter
from app.models import User
from app.onauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import Token, UserCreated, UserLogin
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from ..database import get_db
router = APIRouter(prefix='/user')

@router.post('/register', status_code=status.HTTP_201_CREATED)
def create_user(user : UserCreated, db : Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email, password_hashed=user.password)
    db.add(new_user)
    db.commit()
    return {
        'message' : 'Success, User is Created'
    }

# OAuth2PasswordRequestForm = Depends()
@router.post('/login', response_model=Token)
def user_login(user_data : UserLogin, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'There is no user with this name => {user_data.username}')
    
    if not User.check_password(user.password, user_data.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='your password is invalid')

    token = create_access_token({'user_id':user.id, 'username':user.username, 'email':user.email})

    return {
        'access_token' : token,
        'type_token' : "bearer"
    }