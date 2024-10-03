import astropy.units as u
from astropy.coordinates import SkyCoord
from astroquery.gaia import Gaia
from service.planets import searchPlanet

def starsData(planetN, view_range_x=80, view_range_y=90, dist_range=50):
  planet = searchPlanet(planetN)
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

  stars = []

  for row in results:
    ra = float(row["ra"])
    dec = float(row["dec"])
    distance = float(row["distance_gspphot"])
    stars.append({'ra': ra, 'dec': dec, 'sy_dist': distance})

  return stars