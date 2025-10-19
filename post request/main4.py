from fastapi import FastAPI,HTTPException
from pydantic_schema2 import BandBase, BandCreate, BandwithID, GenreURLChoices
from typing import List

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic','albums':[
        {'title':'Mater of reality','release_date': '1971-01-24'}
    ]},
    {'id': 3, 'name': 'Slowdive', 'genre': 'Classical'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

app = FastAPI()

@app.get('/bands')
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool = False
) -> List[BandwithID]:
    band_list = [BandwithID(**b) for b in BANDS]

    if genre:
        band_list = [
            b for b in band_list if b.genre.lower() == genre.value
        ]
    if has_albums:
        band_list = [
            b for b in band_list
            if len(getattr(b, 'albums', [])) > 0
        ]
    
    return band_list

@app.get('/band/{band_id}')
async def band(band_id: int) -> BandwithID:
    band = next((BandwithID(**b) for b in BANDS if b['id'] == band_id),None)
    if band is None:
        return HTTPException(status_code=404, detail=f'Band with id {band_id} not found')

#post request
@app.post('/bands')
async def create_band(band_data: BandCreate) -> BandwithID:
    id = (max(b['id'] for b in BANDS)+1) if BANDS else 1
    band = BandwithID(id = id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band