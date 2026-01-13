from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #if the user doesn't provide this value it will default to true
    rating: Optional[int] = None #if the user doesn't provide this value it will default to None

#story the data in the memory just for now before moving to database
my_post = [{"id":1,"title": "title of post 1", "content": "content of post 1", "published": True}, 
        {"id":2,"title": "title of post 2", "content": "content of post 2", "published": False}]

@app.get("/")
def root():
    return {"message":"welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data":my_post}

@app.post("/posts")
def create_post(post: Post):
    print(post.dict())
    print(post.title)  #prints in terminal
    print(post.content) #prints in terminal
    print(post.published)
    return {"data":post}
