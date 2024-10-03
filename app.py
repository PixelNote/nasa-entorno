from fastapi import FastAPI
from service.planets import getAllPlanets, searchPlanet
from service.stars import central_reference
from service.simplestars import startsData

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

@app.get("/starsv2/{planetName}")
async def getStars(planetName: str):
  return startsData(planetName);
