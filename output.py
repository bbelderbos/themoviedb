#!/usr/bin/python
# -*- coding: utf-8 -*- 
import os 
from pprint import pprint
import sys

class Output:

  def __init__(self, movies):
    self.posterBaseUrl = "https://image.tmdb.org/t/p/w154" # w92
    self.imdbUrl = "http://imdb.com/title"
    self.sMovies = "http://sharemovi.es"
    self.sMovieUrl = "%s/add_movie_from_email.php?id=" % self.sMovies
    self.sTrailerUrl = "%s/trailer.php?id=MOVIE_ID&link_youtube" % self.sMovies
    self.sPersonUrl = "%s/?personId=" % self.sMovies
    self.movies = movies
    self.maxPersons = {
      "actors" : 5,
      "directors" : 1,
    }

  def _get_persons(self, cast, typePerson="actors"):
    persons = []
    # directors part of crew so need to filter out, cast object has only actors
    if typePerson == "directors":
      cast = [a for a in cast if a["department"].lower() == "directing"]
    for i,c in enumerate(cast):
      persons.append(self._html("a", c["name"], link=self.sPersonUrl+str(c["id"])))
      if typePerson in self.maxPersons and (i+1) == self.maxPersons[typePerson]:
        break
    return persons

  def generate_header(self):
    banner = self._html("a", self._html("img", "%s banner" % self.sMovies, "%s/i/banner.jpg" % self.sMovies), link=self.sMovies)
    return "<h1 style='background-color: #840015;color: #fff;'>%s</h1>" % banner

  def generate_category_title(self, title):
    return "<h2 style='background-color: #C0C0C0; color: #000; padding: 5px;'>%s</h2>" % title

  def generate_movie_html_div(self):
    html = []
    for m,c in self.movies:
      movieId = str(m["id"])
      genres = ", ".join([g["name"] for g in m["genres"]])
      imdbUrl = self._html("a", "imdb", link=os.path.join(self.imdbUrl, m["imdb_id"]))
      sMovieUrl = self._html("a", "add to your sharemovi.es watchlist", link=self.sMovieUrl+movieId)
      sTrailerUrl = self._html("a", "watch trailer", link=self.sTrailerUrl.replace("MOVIE_ID", movieId))
      html.append("<div id='%s'>" % movieId)
      html.append(self._html("h3", m["title"]))
      if genres:
        html.append(self._html("h4", "Genres: " + genres))
      directors = ", ".join(self._get_persons(cast=c["crew"], typePerson="directors"))
      actors = ", ".join(self._get_persons(cast=c["cast"], typePerson="actors"))
      html.append(self._html("h4", "Director: " + directors))
      html.append(self._html("h4", "Actors: " + actors))
      released = "Released: " + m["release_date"]
      html.append(self._html("h5", released + " (" + imdbUrl + " / " + sTrailerUrl + " / " + sMovieUrl + ")"))
      html.append(self._html("p", m["overview"]))
      if m["poster_path"]:
        imgPath = os.path.join(self.posterBaseUrl, m["poster_path"].strip("/"))
        html.append(self._html("img", "poster of " + m["title"], link=imgPath))
      html.append("<br><hr><br>\n</div>")
    return "\n".join(html).encode('utf-8', 'ignore')
        
  def _html(self, tag, name, link=None):
    if tag == "a":
      return "<a target='_blank' href='%s'>%s</a>" % (link, name)
    elif tag == "img":
      return "<img src='%s' alt='%s' />" % (link, name)
    else: 
      return "<%s>%s</%s>" % (tag, name, tag)

if __name__ == "__main__":
  o = Output({})
