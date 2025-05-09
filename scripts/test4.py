import newspaper
import json

url = 'https://ria.ru/20250509/kiev-2016127233.html'
  
article = newspaper.Article(url=url, language='ru')
article.download()
article.parse()
# print(dir(article))

article ={
    "title": str(article.title),
    "text": str(article.text),
    "authors": article.authors,
    "published_date": str(article.publish_date),
    "top_image": str(article.top_image),
    "videos": article.movies,
    "keywords": article.keywords,
    "summary": str(article.summary)
}


for key in article:
    print('-------------------')
    print(f'{key}: {article[key]}')
    print('-------------------\n')