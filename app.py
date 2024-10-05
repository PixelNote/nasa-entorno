from fastapi import FastAPI
from service.planets import getAllPlanets, searchPlanet
from service.stars import central_reference

app = FastAPI()

@app.get("/planets")
def get_planets():
  return getAllPlanets()

@app.get("/planet/{planetName}")
async def getPlanetData(planetName: str):
  return searchPlanet(planetName)

@app.get("/stars/{planetName}")
async def getAllStars(planetName: str):
  return central_reference(planetName);
