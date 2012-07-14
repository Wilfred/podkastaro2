Podkastaro 2 is a port of the original PHP Podkastaro to Django.

Podkastaro is a site that aggregates every Esperanto-language podcast
that I'm aware of. It uses feedparser to fetch the feeds and
BeautifulSoup to remove unwanted text in the descriptions.

The styling is a port of 2Plus, a blogger template developed by Dante
and Klodian.

### Development

    $ pip install -r requirements.txt
    $ python manage.py syncdb
    $ python manage.py runserver

### Future work

* Automatically generated list of all our RSS feeds for those who wish
  to use other RSS apps
* Use bleach to sanitise HTML
* Protect cron/ URLs from external use
* Move to Django 1.4
* Use better names for Django app
* Explore using the built-in MP3 player in browsers that don't support flash
* Unit tests
