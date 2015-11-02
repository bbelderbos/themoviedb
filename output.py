import os 

class Output:

  def __init__(self, movies):
    self.posterBaseUrl = "https://image.tmdb.org/t/p/w92"
    self.imdbUrl = "http://imdb.com/title/"
    self.movies = movies

  def generate_html(self):
    html = []
    for m in self.movies:
      genres = ", ".join([g["name"] for g in m["genres"]])
      if m["poster_path"]:
        imgPath = os.path.join(self.posterBaseUrl, m["poster_path"].strip("/"))
      url = os.path.join(self.imdbUrl, m["imdb_id"])
      html.append("<div>")
      html.append(self._html("h3", m["title"]))
      if genres:
        html.append(self._html("h4", "Genres: " + genres))
      html.append(self._html("h5", "Released: " + m["release_date"]))
      html.append(self._html("p", m["overview"]))
      if m["poster_path"]:
        html.append(self._html("a", imgPath, link=url))
      html.append("</div>")
    return "\n".join(html)
        
  def _html(self, tag, data, link=None):
    attr = ""
    if tag == "a":
      attr = " href='%s'" % link
    elif tag == "img":
      attr = " src='%s'" % link
    return "<%s%s>%s</%s>" % (tag, attr, data, tag)
