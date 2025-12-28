from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic_schema1 import GenreURLChoices,Band
from typing import Optional

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic','albums':[
        {'title':'Mater of reality','release_date': '1971-01-24'}
    ]},
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
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool = False
) -> list[Band]:

    filtered_bands = BANDS  # start with all bands

    # Filter by genre if provided
    if genre:
        filtered_bands = [
            b for b in filtered_bands
            if b['genre'].lower() == genre.value.lower()
        ]

    # Filter by albums if requested
    if has_albums:
        filtered_bands = [
            b for b in filtered_bands
            if len(b.get('albums', [])) > 0
        ]

    if not filtered_bands:
        raise HTTPException(status_code=404, detail="No bands found matching criteria")

    return [Band(**b) for b in filtered_bands]
    


#http://127.0.0.1:8000/bands?genre=rock
#http://127.0.0.1:8000/bands?has_albums=true
#http://127.0.0.1:8000/bands?genre=electronic&has_albums=true
