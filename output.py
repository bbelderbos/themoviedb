import os 

class Output:

  def __init__(self, movies):
    self.posterBaseUrl = "https://image.tmdb.org/t/p/w154" # w92
    self.imdbUrl = "http://imdb.com/title"
    self.smovieUrl = "http://sharemovi.es/?movieId="
    self.movies = movies

  def generate_html(self):
    html = []
    for m in self.movies:
      movieId = str(m["id"])
      genres = ", ".join([g["name"] for g in m["genres"]])
      imdbUrl = self._html("a", "imdb", link=os.path.join(self.imdbUrl, m["imdb_id"]))
      smovieUrl = self._html("a", "sharemovi.es", link=self.smovieUrl+movieId)
      html.append("<div id='%s'>" % movieId)
      html.append(self._html("h3", m["title"]))
      if genres:
        html.append(self._html("h4", "Genres: " + genres))
      released = "Released: " + m["release_date"]
      html.append(self._html("h5", released + " (" + imdbUrl + " / " + smovieUrl + ")"))
      html.append(self._html("p", m["overview"]))
      if m["poster_path"]:
        imgPath = os.path.join(self.posterBaseUrl, m["poster_path"].strip("/"))
        html.append(self._html("img", "poster of " + m["title"], link=imgPath))
      html.append("</div>")
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
