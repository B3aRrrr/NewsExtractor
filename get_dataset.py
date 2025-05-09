from utils.functions import *
from newscatcher import describe_url

import os

test_websites = ['nytimes.com', 'https://ria.ru/']

from config import config

DATASETS_FOLDER = config['default'].DATASETS_FOLDER

for website in test_websites:
   # 1. Получаем информацию об сайте новостей
   url_description = describe_url(website)
   # 2. Создаем папку для записи выборки новостей
   url_dir = os.path.join(DATASETS_FOLDER,url_description['url'])
   if not os.path.exists(url_dir): os.makedirs(url_dir)
   # 3. Записываем информацию о новостях в .txt
   # 4. Извелекаем html страницы новостей
   # 5.

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

from urllib.parse import urlparse

print(urlparse('https://ria.ru/'))