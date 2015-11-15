# Project: python movie weekly email (using themoviedb API) 

[Blog post](http://bobbelderbos.com/2015/11/project-weekly-movie-email-with-tmdbsimple-python/)

    Usage: main.py [options]

    Options:
      -h, --help            show this help message and exit
      -a ACTOR, --actor=ACTOR
                            filter on actor (not yet implemented)
      -c CATEGORY, --category=CATEGORY
                            category [now_playing, upcoming, top_rated, popular]
      -d DIRECTOR, --director=DIRECTOR
                            filter on director (not yet implemented)
      -g GENRES, --genres=GENRES
                            filter on genres (not yet implemented)
      -l LISTING, --listing=LISTING
                            create email from themoviedb list URL
      -m, --mailres         mail the html to recipients
      -n NUMRES, --numres=NUMRES
                            number of results
      -p, --printres        print the html

## Examples

### print html for 10 now_playing movies

    $ python main.py -c now_playing -n 10
    shelve has already movie ID 206647, skipping
    shelve has already movie ID 274854, skipping
    shelve has already movie ID 201085, skipping
    shelving info and credits for new movie ID 361931
    time passed: 1
    less than 2 seconds for 2 requests (max 3 req per second)
    sleep 1 sec to make sure we don't hit the API request limit
    shelving info and credits for new movie ID 227973
    ..

    done shelving
    <h1 style='background-color: #840015;color: #fff;'><a target='_blank' href='http://sharemovi.es'><img src='http://sharemovi.es/i/banner.jpg' alt='http://sharemovi.es banner' /></a></h1>
    <div id='206647'>
    <h3>Spectre</h3>
    <h4>Genres: Action, Adventure, Crime</h4>


### print and email a specific list from themoviedb

    $ python main.py -l https://www.themoviedb.org/list/5637ff1dc3a3681b6101ed43 -pm
    Downloading: https://www.themoviedb.org/list/5637ff1dc3a3681b6101ed43
    shelving info and credits for new movie ID 18785
    time passed: 2
    shelving info and credits for new movie ID 8363
    time passed: 1
    less than 2 seconds for 2 requests (max 3 req per second)
    sleep 1 sec to make sure we don't hit the API request limit
    ..

    done shelving
    <h1 style='background-color: #840015;color: #fff;'><a target='_blank' href='http://sharemovi.es'><img src='http://sharemovi.es/i/banner.jpg' alt='http://sharemovi.es banner' /></a></h1>
    <div id='18785'>
    <h3>The Hangover</h3>
    <h4>Genres: Comedy</h4>
    <h4>Director: <a target='_blank' href='http://sharemovi.es/?personId=57130'>Todd Phillips</a></h4>
    ..

    => emails out the HTML to recipient list
    => for hacker movies use -l https://www.themoviedb.org/list/5637d20d9251414ab701bb61
