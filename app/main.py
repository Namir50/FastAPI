from fastapi import FastAPI, Response,HTTPException
from fastapi.params import Body
import psycopg2
import os
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

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
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s)""", (post.title, post.content, post.published))

@app.get("/post/latest")
def get_latest_post():
    if not my_post:
        return {"error": "No posts found"}
    return {"data": my_post[-1]}

@app.get("/post/{id}")
def get_post(id: int):
    for p in my_post:
        if p['id'] == id:
            return {"data": p}
    raise HTTPException(status_code=404, detail=f"post id {id} not found")
    

@app.delete("/deletepost/{id}")
def delete_post(id: int):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            my_post.pop(i)
            return {"message":"Post deleted"}
        
    raise HTTPException(status_code=404, detail="Post not found")

@app.put("/updatepost/{id}")
def update_post(id:int, updated_post: Post):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            my_post[i]['title'] = updated_post.title
            my_post[i]['content'] = updated_post.content
            return {"message":"Post updated successfully"}
    
    raise HTTPException(status_code=404, detail="Post not found")


    