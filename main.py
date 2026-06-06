from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/health")
def getHealth():
    return {"status":"ok"}

@app.get("/pokemon")
def getPokemon():
    return {"Pokemon": "Pikachu, Charmander, Squirtle, Bulbasaur"}