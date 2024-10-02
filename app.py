from fastapi import FastAPI
from service.planets import getAllPlanets, searchPlanet

app = FastAPI()

@app.get("/planets")
def get_planets():
  return getAllPlanets()

@app.get("/planet/{planetName}")
async def getAllStars(planetName: str):
  return searchPlanet(planetName)