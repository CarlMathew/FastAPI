from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from SQLHandler import APPSql
from schemas import *
from utils import hash_pass

router = APIRouter(tags=["Users"])


@router.get("/user2", status_code=status.HTTP_200_OK)
async def getUser2(payload: GettingID):
    connection = APPSql("SocialMedia")
    query = f"SELECT ID, Email, CreatedAt FROM users2 WHERE ID = {payload.id}"
    result = connection.read_query(query, ())
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def InsertUser(payload: InsertUser):
    connection = APPSql("SocialMedia")
    hashed_password = hash_pass(payload.password)
    payload.password = hashed_password
    query = f""" INSERT INTO users2(Email, Password) VALUES (%s, %s)"""
    connection.insert_query(query, (payload.email, payload.password))
    results = connection.read_query("SELECT ID, Email, CreatedAt FROM users2 ORDER BY ID DESC LIMIT 1", ())[0]
    connection.close_connection()
    return [results]


@router.put("/user_update", status_code=status.HTTP_202_ACCEPTED)
async def UpdateUser(payload: UserUpdate = Depends(UserUpdate)):
    connection = APPSql("SocialMedia")
    hash = hash_pass(payload.password)
    payload.password = hash
    query = f"UPDATE users2 SET Email = %s, Password = %s WHERE ID = %s"
    connection.insert_query(query, (payload.id, payload.email, payload.password))
    return {"data": "Update Successful"}
