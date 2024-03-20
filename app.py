from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "( ͡° ͜ʖ ͡°)  We'll build an API"}

