import shelve
import sys
import time
import tmdbsimple as tmdb

class Cache:
  def __init__(self, category):
    self.category = category
    self.now = int(time.time())

  def _time_passed(self):
    newTime = int(time.time())
    diff = newTime - self.now
    self.now = newTime
    return diff

  def shelve_results(self, movieIds):
    """ 3 req per second, so measure time """
    d = shelve.open(self.category)
    requests = 0
    newMovies = []
    for m in movieIds:
      m = str(m)
      if d.has_key(m):
        print "shelve has already movie ID %s, skipping" % m
        continue
      print "shelving info and credits for new movie ID %s" % m
      newMovies.append(m)
      info = tmdb.Movies(m).info()
      credits = tmdb.Movies(m).credits()
      d[m] = (info, credits)
      requests += 2
      tPassed = self._time_passed()
      print "time passed: %d" % tPassed
      if tPassed < 2:
        print "less than 2 seconds for 2 requests (max 3 req per second)"
        print "sleep 1 sec to make sure we don't hit the API request limit"
        time.sleep(1)
    print "\ndone shelving"
    return newMovies
  
  def shelve_get_items(self, movieIds):
    """ as shelve is unordered, passing in a list of movie Ids to keep order (new to older) """
    out = []
    d = shelve.open(self.category)
    for m in movieIds:
      m = str(m)
      if d.has_key(m):
        out.append(d[m])
    return out
