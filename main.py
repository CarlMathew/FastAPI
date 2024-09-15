from fastapi import FastAPI, status, Depends, HTTPException
# from unused import models
# from unused.database import engine
from fastapi.middleware.cors import CORSMiddleware
from routers import post, user
import auth
import models
from database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
import schemas

#

models.base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    # models.Base.metadata.create_all(bind=engine)
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "https://www.google.com/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"]
)


@app.get("/", status_code=status.HTTP_200_OK)
async def helloWorld():
    return {"status": "Hello World"}


@app.get("/sqlalchemy", status_code=status.HTTP_200_OK)
def test_post(db: Session = Depends(get_db)):
    data = db.query(models.Post).all()
    return {"status": data}


@app.get("/userPost/{id}", status_code=status.HTTP_200_OK)
def specific_test(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    return {"post": data}


@app.get("/titlePost", status_code=status.HTTP_200_OK)
def specific_title(payload: schemas.title = Depends(schemas.title), db: Session = Depends(get_db)):
    data = db.query(models.Post).filter(models.Post.title == payload.title).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Title does not exist")
    return {"post": data}


@app.post("/sqlInsert", status_code=status.HTTP_200_OK)
def test_insert(payload: schemas.Posting, db: Session = Depends(get_db)):
    new_post = models.Post(**payload.dict())
    # print(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"status": new_post}


@app.put("/postUpdate", status_code=status.HTTP_200_OK)
def updatePost(payload: schemas.updatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == payload.id)
    titlePost = post_query.first()
    if titlePost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {payload.id} cannot be found")
    post_query.update(payload.dict(), synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# @app.get("/GetPost", status_code=status.HTTP_200_OK)
# async def GetPost():
#     connection = APPSql("SocialMedia")
#     results = connection.read_query("SELECT * FROM Posts", (None))
#     if not results:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return results
#
#
# @app.get("/RandomPost", status_code=status.HTTP_200_OK)
# async def GetPost():
#     connection = APPSql("SocialMedia")
#     results = connection.read_query("SELECT * FROM Posts", ())
#     random_number = random.randint(1, len(results))
#     final_results = [i for i in results if i["ID"] == random_number]
#     if not results:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#
#     connection.close_connection()
#     return final_results
#
#
# @app.get("/specific", status_code=status.HTTP_200_OK)
# async def SpecificPost(payload: GettingID):
#     connection = APPSql("SocialMedia")
#     results = connection.read_query(f"""SELECT * FROM posts WHERE ID = {payload.id}""", ())
#     if not results:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Joke not found")
#     connection.close_connection()
#     return results
#
#
# @app.get("/userpost", status_code=status.HTTP_200_OK)
# async def UserPost(payload: UserID):
#     connection = APPSql("SocialMedia")
#     results = connection.read_query(f"SELECT * FROM posts WHERE UserID = {payload.userid}", ())
#     if not results:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post Cant Be found")
#     connection.close_connection()
#     return results

#
# @app.get("/user2", status_code=status.HTTP_200_OK)
# async def getUser2(payload: GettingID):
#     connection = APPSql("SocialMedia")
#     query = f"SELECT ID, Email, CreatedAt FROM users2 WHERE ID = {payload.id}"
#     result = connection.read_query(query, ())
#     if not result:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     return result
#
#
# @app.post("/insert", status_code=status.HTTP_201_CREATED)
# async def InsertData(payload: InsertingData):
#     connection = APPSql("SocialMedia")
#     query = """INSERT INTO POSTS(Post, UserID) VALUES (%s, %s)"""
#     success = connection.insert_query(query, (payload.post, payload.userid))
#     if not success:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT)
#     results = connection.read_query("SELECT * FROM posts ORDER BY ID DESC LIMIT 1", ())[0]
#     connection.close_connection()
#     return [results]
#
#
# @app.post("/user", status_code=status.HTTP_201_CREATED)
# async def InsertUser(payload: InsertUser):
#     connection = APPSql("SocialMedia")
#     hashed_password = hash_pass(payload.password)
#     payload.password = hashed_password
#     query = f""" INSERT INTO users2(Email, Password) VALUES (%s, %s)"""
#     connection.insert_query(query, (payload.email, payload.password))
#     results = connection.read_query("SELECT ID, Email, CreatedAt FROM users2 ORDER BY ID DESC LIMIT 1", ())[0]
#     connection.close_connection()
#     return [results]
#
#
# @app.get("/storedProc", status_code=status.HTTP_200_OK)
# async def call_storedProc(payload: StoredProcedure):
#     connection = APPSql("SocialMedia")
#     storeProcName = payload.storedName
#     params = [val for key, val in payload.parameters.items()]
#     results = connection.call_storedproc(storeProcName, params)
#     print(params)
#     print(results)
#     if not results:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post Cant Be found")
#     connection.close_connection()
#     return results


# @app.put("/updatePost", status_code=status.HTTP_202_ACCEPTED)
# async def UpdateData(payload: UpdateData):
#     connection = APPSql("SocialMedia")
#     query = f"UPDATE Posts SET post = %s WHERE ID = %s"
#     connection.insert_query(query, (payload.post, payload.id))
#     connection.close_connection()
#     return {"Status": "Updated"}
#
#
# @app.delete("/delete", status_code=status.HTTP_200_OK)
# async def DeleteData(payload: DeleteData):
#     connection = APPSql("SocialMedia")
#     query = f"""DELETE FROM posts WHERE ID = {payload.id}"""
#     connection.insert_query(query, ())
#     connection.close_connection()
#     return "Done"

# from fastapi import FastAPI, Body, status, HTTPException
# from pydantic import BaseModel
# from typing import Optional, Dict
# import mysql.connector
# from mysql.connector import Error
# from SQLHandler import APPSql
#
#
# app = FastAPI()
#
#
#
# class ReadData(BaseModel):
#     table: str
#     query: str
#
#
# class InsertData(BaseModel):
#     table: str
#     data: Dict[str, str] = None
#
#
# def jSON(result, column):
#     data = []
#     for val in result:
#         m = {}
#         for x, col in zip(val, column):
#             m[col] = x
#         data.append(m)
#     return data
#
#
# @app.get("/read_query", status_code=status.HTTP_201_CREATED)
# async def root(payload: ReadData):
#     connection = APPSql("employees")
#     results = connection.read_query(payload.query)
#     if not results:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     column = [i[0] for i in connection.read_query(f"SHOW COLUMNS FROM {payload.table}")]
#     data = jSON(results, column)
#     return {"data": data}
#
#
# @app.post("/insert", status_code=status.HTTP_201_CREATED)
# async def insert(payload: InsertData):
#     connection = APPSql("employees")
#     data = payload.data
#     mylist = tuple([f"{i}" for i in data.values()])
#     query = f"INSERT INTO {payload.table} VALUES {mylist}"
#     connection.insert_query(query)
#     return {"data": status.HTTP_201_CREATED}
#
#
#
#
#
#
#
