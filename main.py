#!/usr/bin/python
# -*- coding: utf-8 -*- 
from optparse import OptionParser
from pprint import pprint
import sys
from cache import Cache
from mail import Mail
from output import Output
from tmdb import Tmdb

CATEGORIES = ["now_playing", "upcoming", "top_rated", "popular",] 
DEFAULT_CAT = "upcoming"
DEFAULT_NUMRES = 20

def get_value(fname):
  with open(fname,'r') as f:
    return f.read().strip()

def load_emails(fname):
  with open(fname,'r') as f:
    return [email.strip() for email in f.readlines()]
  
def cli():
  parser = OptionParser()
  parser.add_option("-a", "--actor", dest="actor", help="filter on actor")
  parser.add_option("-c", "--category", dest="category", help="category [%s]" % ", ".join(CATEGORIES))
  parser.add_option("-d", "--director", dest="director", help="filter on director")
  parser.add_option("-g", "--genres", dest="genres", help="filter on genres")
  parser.add_option("-n", "--numres", dest="numres", help="number of results")
  (opts, args) = parser.parse_args()
  if not opts.category:
    opts.category = DEFAULT_CAT
  if opts.category not in CATEGORIES:
    sys.exit("%s not in %s" % (opts.category, ", ".join(CATEGORIES)))
  if not opts.numres:
    opts.numres = DEFAULT_NUMRES
  return (opts, args)

def main():
  (opts, args) = cli()
  key = get_value('key')
  td = Tmdb(key, opts.category)
  movies = td.get_movies(opts.numres) 
  ca = Cache(opts.category)
  ca.shelve_results(movies)
  movieObjects = ca.shelve_get_items(movies)
  op = Output(movieObjects)
  html = op.generate_html()
  #print html; sys.exit()
  sender = get_value('sender')
  recipients = load_emails('recipients')
  ma = Mail(sender)
  subject = "%s movie alert" % opts.category.title().replace("_", " ")
  ma.mail_html(recipients, subject, html)

if __name__ == "__main__":
  main() 
