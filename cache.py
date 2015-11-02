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
    for m in movieIds:
      m = str(m)
      if d.has_key(m):
        print "shelve has already movie ID %s, skipping" % m
        continue
      print "shelving new movie ID %s" % m
      d[m] = tmdb.Movies(m).info()
      requests += 1
      if requests % 3 == 0:
        print "3 requests passed, check time passed"
        tPassed = self._time_passed()
        print "time passed: %d" % tPassed
        if tPassed < 1:
          print "less than 1 second for 1 request, sleep 1 sec"
          time.sleep(1)
    print "done"
  
  def shelve_get_items(self, movieIds):
    """ as shelve is unordered, passing in a list of movie Ids to keep order (new to older) """
    out = []
    d = shelve.open(self.category)
    for m in movieIds:
      m = str(m)
      if d.has_key(m):
        out.append(d[m])
    return out
