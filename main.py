#!/usr/bin/python
# -*- coding: utf-8 -*- 
from datetime import date
from optparse import OptionParser
import os
from pprint import pprint
import sys
from cache import Cache
from listing import Listing
from mail import Mail
from output import Output
from tmdb import Tmdb

CATEGORIES = ["now_playing", "upcoming", "top_rated", "popular",] 
DEFAULT_CAT = "upcoming"
DEFAULT_NUMRES = 20
THIS_WEEK = date.today().isocalendar()[1]

def get_value(fname):
  with open(fname,'r') as f:
    return f.read().strip()

def load_emails(fname):
  with open(fname,'r') as f:
    return [email.strip() for email in f.readlines()]
  
def cli():
  parser = OptionParser()
  parser.add_option("-a", "--actor", dest="actor", help="filter on actor (not yet implemented)")
  parser.add_option("-c", "--category", dest="category", help="category [%s]" % ", ".join(CATEGORIES))
  parser.add_option("-d", "--director", dest="director", help="filter on director (not yet implemented)")
  parser.add_option("-g", "--genres", dest="genres", help="filter on genres (not yet implemented)")
  parser.add_option("-l", "--listing", dest="listing", help="create email from themoviedb list URL")
  parser.add_option("-m", "--mailres", dest="mailres", help="mail the html to recipients", action="store_true", default=False)
  parser.add_option("-n", "--numres", dest="numres", help="number of results")
  parser.add_option("-p", "--printres", dest="printres", help="print the html", action="store_true", default=False)
  (opts, args) = parser.parse_args()
  if opts.actor or opts.director or opts.genres:
    sys.exit("Filtering for actor / director / genres not yet implemented") # TODO
  if not opts.category:
    opts.category = DEFAULT_CAT
  if opts.category not in CATEGORIES:
    sys.exit("%s not in %s" % (opts.category, ", ".join(CATEGORIES)))
  if opts.listing:
    opts.category = opts.listing
  if not opts.numres:
    opts.numres = DEFAULT_NUMRES
  return (opts, args)

def main():
  (opts, args) = cli()
  key = get_value('key')
  td = Tmdb(key, opts.category)
  if opts.listing:
    li = Listing(opts.category)
    movies = li.get_movies()
    prefix = "list_"
    subject = "Week %s: %s" % (THIS_WEEK, li.title)
  else:
    movies = td.get_movies(opts.numres) 
    prefix = ""
    subject = "%s movies - week %s" % (opts.category.title().replace("_", " "), THIS_WEEK)
  ca = Cache(prefix + os.path.basename(opts.category))
  newMovies = ca.shelve_results(movies)
  if opts.listing:
    movieObjects = ca.shelve_get_items(movies) # allow dups
  else:
    movieObjects = ca.shelve_get_items(newMovies) # only new ones
  op = Output(movieObjects)
  html = [op.generate_header()]
  html.append(op.generate_movie_html_div())
  if opts.printres:
    print "\n".join(html)
  if opts.mailres:
    sender = get_value('sender')
    recipients = load_emails('recipients')
    ma = Mail(sender)
    ma.mail_html(recipients, subject, "\n".join(html))

if __name__ == "__main__":
  main() 
