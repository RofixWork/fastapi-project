from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.database import get_db
from app.models import User
from app.schemas import TokenData
from .config import settings
from jose import JWTError, jwt
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
# generate token
def create_access_token(data : dict):
    to_encoded = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encoded.update({'exp':expire})

    jwt_encoded = jwt.encode(to_encoded, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encoded

# verify token
def verfiy_access_token(token : str, exeption):
    try:
        jwt_decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = jwt_decoded.get('user_id')
        if user_id is None:
            raise exeption
        token_data = TokenData(id=user_id)
    except JWTError:
        raise exeption

    return token_data

# get curent user
def get_current_user(token:str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verfiy_access_token(token, exeption=credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    return user