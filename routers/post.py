from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from SQLHandler import APPSql
import random
import oauth

from schemas import *

router = APIRouter(tags=["Posts"])





@router.get("/GetPost", status_code=status.HTTP_200_OK)
async def GetPost(users: int = Depends(oauth.get_current_user)):
    connection = APPSql("SocialMedia")
    print(users)
    results = connection.read_query("SELECT * FROM Posts", (None))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return results


@router.get("/RandomPost", status_code=status.HTTP_200_OK)
async def GetPost(users: dict = Depends(oauth.get_current_user)):
    print(users)
    connection = APPSql("SocialMedia")
    results = connection.read_query("SELECT * FROM Posts", ())
    random_number = random.randint(1, len(results))
    final_results = [results[random_number]]
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    connection.close_connection()
    return final_results


@router.get("/specific", status_code=status.HTTP_200_OK)
async def SpecificPost(payload: GettingID = Depends(GettingID)):
    connection = APPSql("SocialMedia")
    results = connection.read_query(f"""SELECT * FROM posts WHERE ID = {payload.id}""", ())
    if not results:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Joke not found")
    connection.close_connection()
    return results


@router.get("/userpost", status_code=status.HTTP_200_OK)
async def UserPost(payload: UserID = Depends(UserID)):
    connection = APPSql("SocialMedia")
    results = connection.read_query(f"SELECT * FROM posts WHERE UserID = {payload.userid}", ())
    if not results:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post Cant Be found")
    connection.close_connection()
    return results


@router.post("/insert", status_code=status.HTTP_201_CREATED)
async def InsertData(payload: InsertingData, userid: int = Depends(oauth.get_current_user)):
    connection = APPSql("SocialMedia")
    query = """INSERT INTO POSTS(Post, UserID) VALUES (%s, %s)"""
    print(type(userid))
    success = connection.insert_query(query, (payload.post, userid["id"]))
    if not success:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    results = connection.read_query("SELECT * FROM posts ORDER BY ID DESC LIMIT 1", ())[0]
    connection.close_connection()
    return [results]


@router.put("/updatePost", status_code=status.HTTP_202_ACCEPTED)
async def UpdateData(payload: UpdateData):
    connection = APPSql("SocialMedia")
    query = f"UPDATE Posts SET post = %s WHERE ID = %s"
    connection.insert_query(query, (payload.post, payload.id))
    connection.close_connection()
    return {"Status": "Updated"}


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def DeleteData(payload: DeleteData):
    connection = APPSql("SocialMedia")
    query = f"""DELETE FROM posts WHERE ID = {payload.id}"""
    connection.insert_query(query, ())
    connection.close_connection()
    return "Done"
