import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from service.planets import searchPlanet
import numpy as np

def central_reference(planetN, view_range_x=15, view_range_y=15, dist_range=20):
  planet = searchPlanet(planetN)
  coord = SkyCoord(ra=planet.get("ra"), dec=planet.get("dec"), unit=(u.degree, u.degree), frame='icrs')
  width = u.Quantity(view_range_x, u.deg)
  height = u.Quantity(view_range_y, u.deg)
  print("Coords: ",coord.ra.deg, coord.dec.deg, width.value, height.value)
  min_dist = 0 if (planet["sy_dist"] - dist_range) < 0 else planet["sy_dist"] - dist_range
  max_dist = planet["sy_dist"] + dist_range
  print("Distancia mínima", min_dist)
  print("Distancia máxima", max_dist)
  query = f"""
  SELECT ra, dec, 
    distance_gspphot,
    phot_g_mean_mag, 
    phot_bp_mean_mag, 
    phot_rp_mean_mag
  FROM gaiadr3.gaia_source
  WHERE 1 = CONTAINS(
    POINT('ICRS', ra, dec),
    BOX('ICRS', {coord.ra.deg}, {coord.dec.deg}, {width.value}, {height.value})
  )
  AND distance_gspphot BETWEEN {min_dist} AND {max_dist}
  """
  r = Gaia.launch_job_async(query)
  results = r.get_results()

  stars = []

  for row in results:
    ra = float(row["ra"])
    dec = float(row["dec"])
    distance = float(row["distance_gspphot"])
    phot_g_mean_mag = float(row["phot_g_mean_mag"])
    phot_bp_mean_mag = float(row["phot_bp_mean_mag"])
    phot_rp_mean_mag = float(row["phot_rp_mean_mag"])
    stars.append({'ra': ra, 
                  'dec': dec, 
                  'distance': distance,
                  'phot_g': phot_g_mean_mag,
                  'phot_bp': phot_bp_mean_mag,
                  'phot_rp': phot_rp_mean_mag})
    
  print(len(stars))

  return stars

