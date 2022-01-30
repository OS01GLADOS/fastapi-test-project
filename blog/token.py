import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from blog.schemas import TokenData


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')))
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode,
                             os.getenv('SECRET_KEY'),
                             algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,
                             os.getenv('SECRET_KEY'),
                             algorithms=[os.getenv('ALGORITHM')])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
       raise credentials_exception
