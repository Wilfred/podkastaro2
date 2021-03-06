# -*- coding: utf-8 -*-
import libs.feedparser

# active podcasts only
podcasts = [('http://www2.polskieradio.pl/podcast/39/podcast.xml', 'Pola Radio'),
            ('http://radioverda.squarespace.com/storage/audio/radioverda.xml', 'Radio Verda'),
            ('http://www.podkasto.net/feed/', 'Varsovia Vento'),
            ('http://parolumondo.com/?feed=podcast', 'Parolu Mondo'),
            ('http://melburno.org.au/3ZZZradio/feed/', '3ZZZ Radio'),
            ('http://www.ameriko.org/eo/rhc/feed', 'Radio Havana Kubo'),
            ('http://la-ondo.rpod.ru/rss.xml', 'Radio Esperanto'),
            ('http://radioaktiva.esperanto.org.uy/?feed=podcast', 'Radio Aktiva'),
            ('http://media01.vatiradio.va/podmaker/podcaster.aspx?c=esperanto_1', 'Radio Vatikana'),
            ('http://media01.vatiradio.va/podmaker/podcaster.aspx?c=esperanto_2', 'Radio Vatikana'),
            ('http://podkastoperposhtelefono.posterous.com/rss.xml', u'Podkasto Per Poŝtelefono'),
            ('http://media.radio-libertaire.org/php/emission.rss.php?emi=59', 'Radio ZAM'),
            ('http://www.panamaradio.org/podkastoj/rss.xml', 'Panama Radio'),
            ("http://feeds.feedburner.com/vej", u'Voĉoj el Japanio')]

feed = libs.feedparser.parse(podcasts[-1][0])

first_entry = feed['entries'][0]
for key in first_entry:
    print "%s: %s\n" % (key.encode('utf-8'), unicode(first_entry[key]).encode('utf-8'))
