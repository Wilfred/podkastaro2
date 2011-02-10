import feedparser

podcast_url = "http://feeds.feedburner.com/vej"

feed = feedparser.parse(podcast_url)

for entry in feed['entries']:
    title = entry['title']
    summary = entry['summary']
    multimedia_items = entry['media_content']

print (title + '\n')
print (summary + '\n')
print (str(multimedia_items) + '\n')
