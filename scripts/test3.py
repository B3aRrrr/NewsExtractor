from newscatcher import Newscatcher, describe_url
import json
import time
from trafilatura import fetch_url, extract

nyt = Newscatcher(website = 'https://ria.ru/')
results = nyt.get_news()

count = 0
articles = results['articles']
for article in articles[:1]:   
   count+=1
   print(
      
     str(count) + ". " + article["title"] \
     + "\n\t\t" + article["published"] \
     + "\n\t\t" + article["link"]\
    #  + "\n\n"
     )
   trafilatura_data_json_str = extract(
      filecontent=fetch_url(article['link']),
      output_format='json',include_comments=True
      )
   print(24,f'trafilatura_data_json_str: {trafilatura_data_json_str}')
   trafilatura_data_json = json.loads(trafilatura_data_json_str)
   for key in trafilatura_data_json:
      print(f'{key}: {trafilatura_data_json[key] if trafilatura_data_json[key] else "NONE"}')
   
   time.sleep(0.33)