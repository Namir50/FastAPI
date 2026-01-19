from fastapi import FastAPI, Response,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
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

@app.post("/posts", status_code=201)  #since status code for creating something is 201
def create_post(post: Post):
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_post.append(post_dict)
    # print(post.title)  #prints in terminal
    # print(post.content) #prints in terminal
    # print(post.published)
    return {"data":post_dict}

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


    