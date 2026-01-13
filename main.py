from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
def root():
    return {"message":"welcome to my api"}

@app.get("/posts")
def get_posts():
    return {"data":"this is your post"}

@app.post("/createpost")
def create_post(new_post: Post):
    print(new_post.title)  #prints in terminal
    print(new_post.content) #prints in terminal
    return {"data":new_post}
