#!/usr/bin/python
# -*- coding: utf-8 -*- 
from datetime import date
import os
from pprint import pprint
import sys
from cache import Cache
from mail import Mail
from main import CATEGORIES, THIS_WEEK, get_value, load_emails
from output import Output
from tmdb import Tmdb

NUM_RES = 20
OUTFILE = os.path.join("weeklies", "week_%s.html" % str(THIS_WEEK))

def main(send=False):
  key = get_value('key')
  html = None
  # get movie info for all categories
  for cat in CATEGORIES:
    td = Tmdb(key, cat)
    movies = td.get_movies(NUM_RES)
    ca = Cache(os.path.basename(cat))
    ca.shelve_results(movies)
    movieObjects = ca.shelve_get_items(movies)
    op = Output(movieObjects)
    if html is None:
      html = [op.generate_header()]
    catPrettified = cat.title().replace("_", " ")
    html.append(op.generate_category_title(catPrettified))
    html.append(op.generate_movie_html_div())
  # save html
  f = open(OUTFILE, "w")
  f.write("\n".join(html))
  f.close() 
  # email
  if send:
    subject = "Sharemovi.es / %s movies / week %s" % (", ".join(CATEGORIES), str(THIS_WEEK))
    sender = get_value('sender')
    recipients = load_emails('recipients')
    ma = Mail(sender)
    ma.mail_html(recipients, subject, "\n".join(html))

if __name__ == "__main__":
  send = False
  if len(sys.argv) > 1:
    send = True
  main(send) 
