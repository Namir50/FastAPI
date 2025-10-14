from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic_schema1 import GenreURLChoices,Band

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Slowdive', 'genre': 'Classical'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands(genre:GenreURLChoices) -> list[Band]:
    if genre:
        return [
            Band(**b) for b in BANDS if b['genre'] == genre.value
        ]
