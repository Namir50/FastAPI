from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel
from datetime import date

class GenreURLChoices(Enum):  
    Rock= 'rock'
    Electronic = 'electronic'
    Classical = 'classical'
    HipHop = 'hip-hop'


class Album(BaseModel):
    title:str
    release_date: date

class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Album]  = [] #default empty list

