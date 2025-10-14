from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic_schema1 import GenreURLChoices,Band
from typing import Optional

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Slowdive', 'genre': 'Classical'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

#without pydantic
@app.get('/basicbands')
async def basicbands(genre: Optional[str]=None):
    if genre:
        return[
        b for b in BANDS if b['genre'].lower() == genre.lower()
        ]
    return BANDS

#query parameter lets you use the same endpoint for multiple behaviors, depending on what parameters are passed
#with pydantic
@app.get('/bands')
async def bands(genre:GenreURLChoices | None = None) -> list[Band]:
    if genre:
        return [
            Band(**b) for b in BANDS if b['genre'].lower() == genre.value
        ]
    return [Band(**b) for b in BANDS]
