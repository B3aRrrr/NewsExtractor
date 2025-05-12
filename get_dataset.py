from utils.functions import *
from newscatcher import Newscatcher, describe_url
import json
import time
from trafilatura import fetch_url, extract
import os

test_websites = ['nytimes.com', 'https://ria.ru/']

from config import config

DATASETS_FOLDER = config['default'].DATASETS_FOLDER

for website in test_websites:
   # 1. Получаем информацию об сайте новостей
   url_description = describe_url(website)
   # 2. Создаем папки для записи выборки новостей
   url_dir = os.path.join(DATASETS_FOLDER,url_description['url'])
   if not os.path.exists(url_dir): 
      os.makedirs(url_dir)
   html_raw = os.path.join(url_dir,'html_raw')
   if not os.path.exists(html_raw): 
      os.makedirs(html_raw)
   gold_standard = os.path.join(url_dir,'gold_standard') 
   if not os.path.exists(gold_standard): 
      os.makedirs(gold_standard)
   extracted_texts = os.path.join(url_dir,'extracted_texts') 
   if not os.path.exists(extracted_texts): 
      os.makedirs(extracted_texts)
   # 3. Получаем список новостей с сайта
   nyt = Newscatcher(website = url_description['url'])
   results = nyt.get_news()
   articles = results['articles']
   for article in articles[:10]:
      name_article = get_title_from_url(article["link"])
      url_article = article["link"]
      # 3. Записываем информацию о новостях в .txt
      with open(os.path.join(url_dir,'urls.txt'), 'a') as f:
         f.write(url_article)
         f.write('\n')
      # 4. Извлекаем html страницы новостей в папку html-raw 
      URL2HTML(
          url=url_article,
          output_path=html_raw,
          name=name_article
      )
      # 5. Создаем и заполняем папку extracted_texts содержимыми новостей
      try:
         trafilatura_data_json_str = extract(
            filecontent=fetch_url(article['link']),
            output_format='json', include_comments=True)
         
         print(54, f'trafilatura_data_json_str: {trafilatura_data_json_str}')
         trafilatura_data_json = json.loads(trafilatura_data_json_str)
         if 'text' in trafilatura_data_json:
            with open(file=os.path.join(extracted_texts, f'{describe_url(article["link"])["url"]}.txt'),mode='w') as f:
               f.write(trafilatura_data_json['text'])        
         else:
            print(f"Ключ 'text' не найден в данных для статьи: {article['link']}")
      except Exception as e:
        print(f"Ошибка при обработке статьи {article['link']}: {e}")

# print(urls)

# import feedparser
# import time
# if len(urls) > 0:
#   news_feed = feedparser.parse(urls[0])
#   entries = news_feed["entries"]
#   count=0
#   for entry in entries:
#     count = count + 1
#     print(
#      str(count) + ". " + entry["title"] \
#      + "\n\t\t" + entry["published"] \
#      + "\n\t\t" + entry["link"]\
#      + "\n\n"
#      )
#     time.sleep(0.33)
