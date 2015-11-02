from bs4 import BeautifulSoup as Soup
import re                                                                           
import sys
import urllib2

class Listing:

  def __init__(self, url):
    self.html = self._download(url)
    self.s = Soup(self.html, "html5lib")
    self.p = re.compile(r'^\d+$') # find all lis with id of numeric string
    self.title = self._get_title()

  def get_movies(self):
    ids = self.s.find_all("li", {"id": self.p})
    return [i["id"] for i in ids]

  def _get_title(self):
    return re.sub(r'([A-Za-z0-9 ]+).*' , r'\1', self.s.find("title").get_text()).strip().title()

  def _download(self, url, user_agent='wswp', num_retries=2):
    """ from http://techbus.safaribooksonline.com/book/programming/python/9781782164364 """
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
      html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
      print 'Download error:', e.reason
      html = None
      if num_retries > 0:
        if hasattr(e, 'code') and 500 <= e.code < 600:
          # retry 5XX HTTP errors
          return self._download(url, user_agent, num_retries-1)
    return html

if __name__ == "__main__":
  print "hacker movies"
  url = "https://www.themoviedb.org/list/5637d20d9251414ab701bb61"
  li = Listing(url)
  print li.get_movies()
