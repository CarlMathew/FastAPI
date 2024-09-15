from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import *
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from SQLHandler import APPSql

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
# Secret_Key
# Algorithm
# ExpirationTime
SECRET_KEY = "c01b3d69a6da677d42d4a61d9c844fe24dfba0c717ff7832688150d716044225"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("userid")

        if id is None:
            raise credentials_exception
        token_data = {"id": id}
        return token_data
    except JWTError as e:
        raise credentials_exception



def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Unable to validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_token_access(token, credentials_exception)
    users_id = token["id"]
    connection = APPSql("socialmedia")
    results = connection.read_query(f"SELECT * FROM users2 WHERE ID = %s", [users_id])
    return results


