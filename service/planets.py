import requests

def getAllPlanets():
  URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+unique(pl_name)+from+ps&format=json"
  response = requests.get(URL)
  if response.status_code == 200:
    print("Solicitud exitosa!")
    return response.json()
  else:
    print("Error con la solicitud!")

def searchPlanet(planetName):
  result = {}
  response = requests.get(f'https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+unique(pl_name),ra,dec,sy_dist+from+ps+where+pl_name+=+\'{planetName}\'&format=json')
  if response.status_code == 200:
    result.update(response.json()[0])
    return result
  else:
    print("Error con el planeta!")