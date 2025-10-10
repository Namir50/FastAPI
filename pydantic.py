from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

class GenreURLChoices(Enum):  
    Rock= 'rock'
    Electronic = 'electronic'
    Classical = 'classical'
    HipHop = 'hip-hop'