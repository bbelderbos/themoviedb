#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os
from optparse import OptionParser
from pprint import pprint
import shelve
import sys
import tmdbsimple as tmdb
import math

class Utils:
  def __init__(self):
    pass

  def roundup(self, num):
    return int(math.ceil(num))

class TmDb:
  def __init__(self):
    self.keyFile = 'key'
    tmdb.API_KEY = self._get_api_key()
    self.m = tmdb.Movies()
    self.u = Utils()
    self.categories = ["now_playing", "upcoming", "top_rated", "popular",] 
    self.resPerQuery = 20

  def _get_api_key(self):
    with open(self.keyFile,'r') as f:
      return f.read().strip()

  def _get_num_pages(self, numres):
    try:
      numres = float(numres)
    except ValueError:
      sys.exit("Cannot convert number to float")
    return self.u.roundup(numres/self.resPerQuery) 

  def get_movies(self, category, numres):
    pages = self._get_num_pages(numres)
    for i in range(1, pages+1): 
      res = getattr(self.m, category)(page=i)
      # pprint(res); sys.exit()
      self._shelve_results(category, res["results"])

  def _shelve_results(self, fname, res):
    d = shelve.open(fname)
    for r in res:
      movieId = str(r["id"])
      if not d.has_key(movieId):
        print "shelving movie ID %s" % movieId
        d[movieId] = r
    print "done"

  def get_movie_info(self, movieId):
    m = tmdb.Movies(movieId)
    res = m.info()  
    pprint(res)
    # print "credits"
    # pprint(m.credits())


if __name__ == "__main__":
  td = TmDb()
  parser = OptionParser()
  parser.add_option("-a", "--actor", dest="actor", help="filter on actor")
  parser.add_option("-c", "--category", dest="category", help="category [%s]" % ", ".join(td.categories))
  parser.add_option("-d", "--director", dest="director", help="filter on director")
  parser.add_option("-g", "--genres", dest="genres", help="filter on genres")
  parser.add_option("-n", "--numres", dest="numres", help="number of results")

  (opts, args) = parser.parse_args()
  if not opts.category:
    opts.category = "upcoming"
  if opts.category not in td.categories:
    sys.exit("%s not in %s" % (opts.category, ", ".join(td.categories)))
  filters = {
    "actor" : opts.actor, 
    "director" : opts.director, 
    "genres" : opts.genres, 
  }
  if not opts.numres:
    opts.numres = 20
  td.get_movies(category=opts.category, numres=opts.numres)
  #td.get_movie_info(206647)
