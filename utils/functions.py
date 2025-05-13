import requests
from tkinter import filedialog as fd
from tkinter import Tk 
import trafilatura
from langdetect import detect
from difflib import SequenceMatcher

import nltk
nltk.download('punkt')
nltk.download('punkt_ru')
nltk.download('punkt_tab')

from nltk.tokenize import sent_tokenize

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def is_similar(sent1, sent2, threshold=0.8):
    """
    Проверяет, являются ли два предложения похожими на основе коэффициента сходства.

    :param sent1: Первое предложение для сравнения.
    :param sent2: Второе предложение для сравнения.
    :param threshold: Пороговое значение коэффициента сходства (от 0 до 1), выше которого предложения считаются похожими.
    :return: True, если коэффициент сходства >= threshold, иначе False.
    """
    return SequenceMatcher(None, sent1, sent2).ratio() >= threshold

def evaluate_extraction(reference_text:str, extracted_text:str, similarity_threshold:float=0.8) -> dict:
    """
    Оценивает полноту извлечения текста, сравнивая извлечённый текст с эталонным.

    :param reference_text: Эталонный текст (полный текст новости).
    :param extracted_text: Извлечённый текст, полученный из парсера/скрапинга.
    :param similarity_threshold: Порог коэффициента сходства предложений для их сопоставления.
    :return: Словарь с результатами оценки:
             - "recall": доля совпадающих предложений из эталона (0–1),
             - "missing_sentences": список пропущенных (не найденных) предложений,
             - "matched_count": количество совпадающих предложений,
             - "total_reference": общее количество предложений в эталонном тексте.
    """
    language = detect(reference_text)  # Определяем язык
    if language == 'ru':
        language= 'russian'
    reference_sentences = sent_tokenize(reference_text, language=language)
    extracted_sentences = sent_tokenize(extracted_text, language=language)

    matched = []
    missing = []

    for ref_sent in reference_sentences:
        if any(is_similar(ref_sent, ext_sent, similarity_threshold) for ext_sent in extracted_sentences):
            matched.append(ref_sent)
        else:
            missing.append(ref_sent)

    recall = len(matched) / len(reference_sentences) if reference_sentences else 0.0

    return {
        "recall": round(recall, 3),
        "missing_sentences": missing,
        "matched_count": len(matched),
        "total_reference": len(reference_sentences)
    }

def extract_article(url:str, headers:dict) -> str:
    """
        Функция извлечения текста статьи из URL-ссылки

    Args:
        url (str): URL новостной статьи
        headers (dict): User-Agent для запросов к браузеру

    Returns:
        str: Текст эталонной новости
    """
    try:
        # Загружаем HTML страницы с указанными заголовками
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Извлекаем контент с помощью trafilatura
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            # Парсим страницу, чтобы извлечь только основной текст статьи
            article = trafilatura.extract(downloaded)

            # Если статья не была найдена, вернем пустой результат
            if article:
                # Получаем мета-данные, включая заголовок
                metadata = trafilatura.extract_metadata(downloaded)
                title = metadata.title if metadata and hasattr(metadata, 'title') else 'Без заголовка'

                # Определяем язык текста
                language = detect(article)
                return {
                    'title': title,
                    'text': article,
                    'language': language
                }
            else:
                print("[!] Текст не был извлечён")
                return None
        else:
            print("[!] Не удалось загрузить страницу")
            return None

    except requests.exceptions.RequestException as e:
        print(f"[!] Ошибка при запросе страницы: {e}")
        return None

def select_file() -> str:
    """Открывает диалоговое окно для выбора файла Excel и возвращает его путь."""
    root = Tk()
    root.withdraw()  # Скрыть главное окно
    file_path = fd.askopenfilename(
        title="Выберите Excel файл",
        filetypes=[("Excel files", "*.xls;*.xlsx")])
    root.destroy()  # Закрыть главное окно
    return file_path

def get_embedding(text:str):
    """
    Получает эмбеддинг для заданного текста с помощью модели SentenceTransformer.

    :param text: Текст для кодирования.
    :return: Вектор-эмбеддинг (numpy-массив) длины 384.
    """
    return model.encode([text])[0]

def semantic_similarity(text1, text2):
    """
    Вычисляет косинусное сходство между двумя текстами на основе эмбеддингов.

    :param text1: Первый текст.
    :param text2: Второй текст.
    :return: Значение косинусного сходства от 0 до 1, где 1 — полная семантическая идентичность.
    """
    return cosine_similarity([get_embedding(text1)], [get_embedding(text2)])[0][0]

def evaluate_significance(reference_text: str, extracted_text: str, threshold: float = 0.8):
    """
    Оценивает семантическую значимость пропущенных фрагментов статьи по сравнению с эталоном.

    Для каждого пропущенного предложения вычисляется его вклад в повышение семантического сходства
    между извлечённым и эталонным текстом.

    :param reference_text: Полный текст статьи (эталон).
    :param extracted_text: Извлечённый скрапером текст.
    :param threshold: Порог (не используется напрямую в текущей реализации, зарезервирован для расширения).
    :return: Словарь с результатами:
             - "semantic_similarity": косинусное сходство между извлечённым и эталонным текстом,
             - "missing_fragments": список словарей с пропущенными предложениями и их вкладом в семантику ("semantic_gain").
               Сортированы по убыванию вклада.
    """
    language = detect(reference_text)
    if language == 'ru':
        language= 'russian'
    ref_sentences = sent_tokenize(reference_text, language=language)
    ext_sentences = sent_tokenize(extracted_text, language=language)

    # Найти пропущенные предложения
    missing = []
    for ref_sent in ref_sentences:
        if all(ref_sent not in ext_sent for ext_sent in ext_sentences):
            missing.append(ref_sent)

    # Эмбеддинги
    full_embed = get_embedding(reference_text)
    extracted_embed = get_embedding(extracted_text)
    original_similarity = cosine_similarity([full_embed], [extracted_embed])[0][0]

    results = []

    for sent in missing:
        new_text = extracted_text + " " + sent
        new_embed = get_embedding(new_text)
        new_similarity = cosine_similarity([full_embed], [new_embed])[0][0]
        gain = new_similarity - original_similarity

        results.append({
            "sentence": sent,
            "semantic_gain": round(gain, 4)
        })

    # Сортируем по значимости
    results.sort(key=lambda x: x['semantic_gain'], reverse=True)

    return {
        "semantic_similarity": round(original_similarity, 4),
        "missing_fragments": results
    }
