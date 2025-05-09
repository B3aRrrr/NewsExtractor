from newscatcher import Newscatcher, describe_url
import json
import time

nyt = Newscatcher(website = 'https://ria.ru/')
results = nyt.get_news()

count = 0
articles = results['articles']
for article in articles[:5]:   
   count+=1
  #  for key in article:
      # print(f'{key}: {article[key]}')
   print(
      
     str(count) + ". " + article["title"] \
     + "\n\t\t" + article["published"] \
     + "\n\t\t" + article["link"]\
    #  + "\n\n"
     )
   time.sleep(0.33)