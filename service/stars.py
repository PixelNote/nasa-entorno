import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from service.planets import searchPlanet
import numpy as np

def cartesian(ra, dec, dist):
  ra_rad = np.radians(ra)
  dec_rad = np.radians(dec)

  x = dist * np.cos(dec_rad) * np.cos(ra_rad)
  y = dist * np.cos(dec_rad) * np.sin(ra_rad)
  z = dist * np.sin(dec_rad)

  return x, y, z


def trasladar_coordenadas(star, punto_inicial):
  x_inicial, y_inicial, z_inicial = punto_inicial
  x0, y0, z0 = star

  x = x0 - x_inicial
  y = y0 - y_inicial
  z = z0 - z_inicial

  return x, y, z


def central_reference(planet, view_range_x=100, view_range_y=100, dist_range=100):
  planet = searchPlanet(planet)
  x1, y2, z3 = cartesian(planet.get("ra"), planet.get("dec"), planet.get("sy_dist"))

  print(x1,y2,z3)

  coord = SkyCoord(ra=planet.get("ra"), dec=planet.get("dec"), unit=(u.degree, u.degree), frame='icrs')
  width = u.Quantity(view_range_x, u.deg)
  height = u.Quantity(view_range_y, u.deg)
  min_dist = 0 if (planet["sy_dist"] - dist_range) < 0 else planet["sy_dist"] - dist_range
  max_dist = planet["sy_dist"] + dist_range
  query = f"""
  SELECT ra, dec, distance_gspphot
  FROM gaiadr3.gaia_source
  WHERE 1 = CONTAINS(
    POINT('ICRS', ra, dec),
    BOX('ICRS', {coord.ra.deg}, {coord.dec.deg}, {width.value}, {height.value})
  )
  AND distance_gspphot BETWEEN {min_dist} AND {max_dist}
  """
  r = Gaia.launch_job_async(query)
  results = r.get_results()

  coords = []

  coords.append({'ra': x1, 'dec': y2, 'dist': z3})

  for row in results:
    ra = row["ra"]
    dec = row["dec"]
    distance = row["distance_gspphot"]
    cartesian_star_points = cartesian(ra , dec, distance)
    x, y, z = trasladar_coordenadas(cartesian_star_points,[x1,y2,z3])


    coords.append({'ra': x, 'dec': y, 'dist': z})

  

  return coords

