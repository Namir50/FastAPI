from fastapi import FastAPI, HTTPException  #HTTPEXCEPTION IS FOR ERROR HANDLING
from enum import Enum

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Slowdive', 'genre': 'Classical'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands() -> list[dict]:
    return BANDS

#fetching individual band
@app.get('/band/{band_id}')
async def band(band_id: int) ->dict:
    band = next((b for b in BANDS if b['id']==band_id),None)
    if band is None:
        #status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band

class GenreURLChoices(Enum):  #using enum to take predefined genre categories or values
    Rock= 'rock'
    Electronic = 'electronic'
    Classical = 'classical'
    HipHop = 'hip-hop'

#fetching band based on genre
@app.get('/band/genre/{genre}')
async def band_genre(genre: GenreURLChoices) -> list[dict]:
    band_by_genre = [b for b in BANDS if b['genre'].lower() == genre.value]
    if not band_by_genre:
        raise HTTPException(status_code=404, detail='No band with this genre')
    return band_by_genre