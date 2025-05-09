from feedsearch import search
feeds = search('https://ria.ru/')
urls = [f.url for f in feeds]

print(urls)

import feedparser
import time
if len(urls) > 0:
  news_feed = feedparser.parse(urls[0])
  entries = news_feed["entries"]
  count=0
  for entry in entries:
    count = count + 1
    print(
     str(count) + ". " + entry["title"] \
     + "\n\t\t" + entry["published"] \
     + "\n\t\t" + entry["link"]\
     + "\n\n"
     )
    time.sleep(0.33)