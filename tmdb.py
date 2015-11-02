import math
import sys
import tmdbsimple as tmdb

class Tmdb:
  def __init__(self, key, category):
    tmdb.API_KEY = key
    self.category = category
    self.m = tmdb.Movies()
    self.resPerQuery = 20

  def _get_num_pages(self, numres):
    try:
      return int(math.ceil(float(numres)/self.resPerQuery))
    except ValueError:
      sys.exit("Cannot convert number to float")

  def _get_latest_movie_ids(self, results):
    return [r["id"] for r in results]

  def get_movies(self, numres): 
    movies = []
    for i in range(1, self._get_num_pages(numres) + 1): 
      res = getattr(self.m, self.category)(page=i)
      movieIds = self._get_latest_movie_ids(res["results"])
      movies += movieIds
    return movies

if __name__ == "__main__":
  pass
