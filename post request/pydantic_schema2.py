from pydantic import BaseModel
from datetime import date
from enum import Enum

class GenreURLChoices(Enum):  
    Rock= 'rock'
    Electronic = 'electronic'
    Classical = 'classical'
    HipHop = 'hip-hop'


class Album(BaseModel):
    title: str
    release_date = date

class BandBase(BaseModel):
    name: str
    genre: str
    albums: list[Album] = []

class BandCreate(BandBase):
    pass

class BandwithID(BandBase):
    id: int