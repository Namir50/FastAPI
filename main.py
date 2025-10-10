from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def index() ->dict[str,str]:  #output datatype is used for data type verification or checking
    return {'hello':'world'}

@app.get('/about')
async def about() -> str:
    return 'An exceptional company'