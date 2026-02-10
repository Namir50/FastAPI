from fastapi import FastAPI, Response,HTTPException, Depends
from fastapi.params import Body
import psycopg2
import os
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()

def get_db():
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #if the user doesn't provide this value it will default to true
    rating: Optional[int] = None #if the user doesn't provide this value it will default to None

while True:
    try: 
        conn = psycopg2.connect(host=os.getenv('DATABASE_HOST'), 
                                    database=os.getenv('DATABASE_NAME'), 
                                    user=os.getenv('DATABASE_USER'), password=os.getenv('DATABASE_PASSWORD'),
                                    cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connected successfully")
        break
        
    except Exception as error:
        print("Database connnection failed")
        print("Error ",error)
        time.sleep(2)

#story the data in the memory just for now before moving to database
my_post = [{"id":1,"title": "title of post 1", "content": "content of post 1", "published": True}, 
        {"id":2,"title": "title of post 2", "content": "content of post 2", "published": False}]

@app.get("/")
def root():
    return {"message":"welcome to my api"}

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status":"success"}

@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    # print(posts)
    # return {"data":my_post}
    return {"data":posts}

@app.post("/posts", status_code=201)  #since status code for creating something is 201
def create_post(post: Post):
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_post.append(post_dict)
    # # print(post.title)  #prints in terminal
    # # print(post.content) #prints in terminal
    # # print(post.published)
    # return {"data":post_dict}
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s)  RETURNING * """, 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

    

@app.get("/post/latest")
def get_latest_post():
    if not my_post:
        return {"error": "No posts found"}
    return {"data": my_post[-1]}

@app.get("/post/{id}")
def get_post(id: int):
    # for p in my_post:
    #     if p['id'] == id:
    #         return {"data": p}
    # raise HTTPException(status_code=404, detail=f"post id {id} not found")
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    post = cursor.fetchone()
    if not post:
        return HTTPException(status_code=404,detail = f"post with {id} not found")
    return {"data" :post}


@app.delete("/deletepost/{id}")
def delete_post(id: int):
    # for i, p in enumerate(my_post):
    #     if p['id'] == id:
    #         my_post.pop(i)
    #         return {"message":"Post deleted"}
        
    # raise HTTPException(status_code=404, detail="Post not found")
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))
    deleted_post = cursor.fetchone()

    if not deleted_post:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
        
    conn.commit()
    return {"data": deleted_post, "message": "Post deleted successfully"}


@app.put("/updatepost/{id}")
def update_post(id:int, post: Post):
    # for i, p in enumerate(my_post):
    #     if p["id"] == id:
    #         my_post[i]['title'] = updated_post.title
    #         my_post[i]['content'] = updated_post.content
    #         return {"message":"Post updated successfully"}
    
    # raise HTTPException(status_code=404, detail="Post not found")S
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING *""", (post.title, post.content, post.published))
    updated_post = cursor.fetchone()
    
    if updated_post is None:
        raise HTTPException(status_code=404, detail=f"post with id {id} not found")
    
    conn.commit()
    return {"data": updated_post, "message": "Post updated successfully"}


    