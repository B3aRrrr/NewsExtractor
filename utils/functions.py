import os
import requests
from urllib.parse import urlparse, unquote

def URL2HTML(url: str, output_path: str = os.getcwd(), name: str = 'test') -> None:
    """
    Загружает HTML страницы по URL с помощью requests и сохраняет в файл.

    Args:
        url (str): URL страницы.
        output_path (str): Путь к папке для сохранения.
        name (str, optional): Имя файла без расширения. По умолчанию 'test'.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'[URL2HTML] Ошибка при запросе URL {url}: {e}')
        return

    os.makedirs(output_path, exist_ok=True)
    file_path = os.path.join(output_path, f'{name}.html')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f'[URL2HTML] HTML сохранён в {file_path}')
    except IOError as e:
        print(f'[URL2HTML] Ошибка при записи файла {file_path}: {e}')

def get_title_from_url(url: str) -> str:
    """
        Загружаем URL страницы и возвращаем её краткое ID-название

    Args:
        url (str): URL страницы.

    Returns:
        str: Краткое ID-название
    """
    parsed_url = urlparse(url)
    path = parsed_url.path  # Например: /2025/05/12/business/china-us-tariffs.html
    # Разбиваем путь на части
    parts = path.rstrip('/').split('/')
    filename = parts[-1]  # Например: 'china-us-tariffs.html'
    # Удаляем расширение
    title = os.path.splitext(filename)[0]
    # Можно дополнительно декодировать URL
    title = unquote(title)
    return title

