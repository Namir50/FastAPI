from fastapi import FastAPI,HTTPException
from pydantic_schema import Band, GenreURLChoices

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Slowdive', 'genre': 'Classical'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands() -> list[Band]:
    return [
        Band(**b) for b in BANDS  #unpacking  data for pydantic
    ]

#fetching individual band
@app.get('/band/{band_id}')
async def band(band_id: int) ->Band:
    band = next((Band(**b) for b in BANDS if b['id']==band_id),None)
    if band is None:
        #status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band