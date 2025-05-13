from utils.functions import *


# Пример использования
url = "https://ria.ru/20250512/dnr-2016505307.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

result = extract_article(url, headers)
if result:
    print("=== Заголовок ===")
    print(result['title'])
    print("=== Язык ===")
    print(result['language'])
    print("=== Текст статьи ===")
    print(result['text'])

