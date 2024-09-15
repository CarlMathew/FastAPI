from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import oauth
import utils
from SQLHandler import APPSql
from schemas import *
from utils import *
from oauth import *
router = APIRouter(tags=["Authentication"])




@router.post("/login", status_code=status.HTTP_201_CREATED)
def login(user_credential: OAuth2PasswordRequestForm = Depends()):
    connection = APPSql("SocialMedia")
    result = connection.read_query(f"SELECT * FROM Users2 WHERE Email = '{user_credential.username}'",
                                   ())
    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify(user_credential.password, result[0]["Password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    access_token = oauth.create_access_token(data={"userid": result[0]["ID"]})
    return {"Token": access_token, "token_type": "bearer"}