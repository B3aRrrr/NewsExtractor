# 📰 NewsExtractor

Проект для оценки качества извлечения текста новостных статей из URL-адресов. Позволяет сравнить результат работы сторонней библиотеки с "эталонным" текстом, извлечённым через `trafilatura`, оценить **полноту извлечения** и **значимость пропущенных фрагментов**, а также сохранить результат в удобном формате.

---

## 🎯 Цель проекта

Создание простого в использовании сервиса, который:

- получает на вход Excel-файл со списком URL и результатами стороннего извлечения;
- извлекает "эталонный" текст с помощью [trafilatura](https://github.com/adbar/trafilatura);
- сравнивает с результатами сторонней библиотеки;
- оценивает полноту совпадения;
- оценивает важность недостающих частей (на основе `nltk`, `difflib` и др.);
- сохраняет результат в новый `.xlsx` файл с суффиксом `_output`.

---

## 🛠 Используемые технологии

- Python 3.9.2  
- [trafilatura](https://pypi.org/project/trafilatura/) — извлечение основного текста с web-страниц  
- [langdetect](https://pypi.org/project/langdetect/) — определение языка  
- [difflib](https://docs.python.org/3/library/difflib.html) — сравнение текстов  
- [nltk](https://www.nltk.org/) — работа с лингвистическими структурами (токены, частотный анализ)  
- [pandas](https://pandas.pydata.org/) — работа с таблицами  
- [openpyxl](https://openpyxl.readthedocs.io/) — сохранение Excel-файлов

---

## 📂 Структура проекта

```bash
NewsExtractor/
│
├── main.py                 # 💡 Основной скрипт запуска 
├── config.py               # 📥 Конфигурационные параметры проекты (пути к данным, параметры User-Agent, параметры модели)
├── utils/                  # 🧰 Вспомогательные функции
│   ├── __init__.py
│   ├── functions.py
│   └── scrapegraphai_functions.py
│
├── data/              # 📁 Примеры Excel-файлов до и после обработки
│   ├── Test_check.xlsx
│   └── Test_check_output.xlsx
│
├── README.md              # 📘 Документация проекта
└── requirements.txt       # 📦 Список зависимостей
```

---

## 🚀 Быстрый старт

1. Клонируй репозиторий:

```bash
git clone https://github.com/B3aRrrr/NewsExtractor.git
cd NewsExtractor
```

2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Запусти обработку:

```bash
py main.py --excel_data_path path/to/input_file.xlsx
```

На выходе появится файл `input_file_output.xlsx` c новыми колонками:

- `gold_standard`
- `recall`
- `loss_significance`

---

## 📊 Пример результата

Исходный файл:
![screenshot](https://github.com/B3aRrrr/NewsExtractor/blob/main/data/Test_check.png)

Результат:
![screenshot](https://github.com/B3aRrrr/NewsExtractor/blob/main/data/Test_check_output.png)

---

## 📐 Метрики

1. **Полнота извлечения (Recall)**
**Определение**:
*Полнота оценивает насколько извлеченный текст покрывает предложения из оригинального (эталонного) текста*
**Формула**:

![Recall](https://github.com/B3aRrrr/NewsExtractor/blob/main/data/Recall.png)

где:

- `TP` — количество истинно положительных (количество совпадающих предложений),
- `FN` — количество ложно отрицательных (общее количество предложений в эталоне минус количество совпадающих предложений).

**Реализация**:

- Функция: `evaluate_extraction()`

- Используется библиотека `difflib.SequenceMatcher` для сравнения предложений

- Сравнение идет по всем предложениям эталонного текста и считается, какие из них присутствуют в извлеченном тексте с похожестью более 0.8

**Возвращаемые значения**:

```python
{
  "recall": 0.78,                        # Доля покрытых предложений
  "missing_sentences": [...],           # Список пропущенных предложений
  "matched_count": 18,                  # Кол-во совпадающих предложений
  "total_reference": 23                 # Общее число предложений в эталоне
}
```

2. **Значимость пропущенных фрагментов (Semantic Loss / Semantic Gain)**
**Определение**:
*Не все пропущенные предложения одинаково важны. Данная метрика оценивает, насколько каждое из них влияет на семантическое сходство между извлечённым текстом и полным эталонным текстом.*
**Формула**:

![Semantic Gain](https://github.com/B3aRrrr/NewsExtractor/blob/main/data/Semantic_gain.png)

**Реализация**:

- Функция: `evaluate_significance()`

- Используется модель `paraphrase-multilingual-MiniLM-L12-v2` из библиотеки `sentence-transformers`

- Строятся эмбеддинги для полного эталонного текста и извлеченного текста

- Затем поочередно добавляются пропущенные предложения, и измеряется прирост косинусного сходства - это и есть `semantic_gain` для каждого предложения

**Возвращаемые значения**:

```python
{
  "semantic_similarity": 0.83,              # Исходное семантическое сходство
  "missing_fragments": [
    {"sentence": "Президент заявил, что...", "semantic_gain": 0.0321},
    {"sentence": "Это может повлиять на ...", "semantic_gain": 0.0183},
    ...
  ]
}

```

---

## 🔧 Возможные улучшения

- Web-интерфейс
- Использование методов извлечение основанных [ScrapeGraphAI](https://github.com/ScrapeGraphAI/Scrapegraph-ai) (метод основанный на использовании данного способа [реализован](https://github.com/B3aRrrr/NewsExtractor/blob/main/utils/scrapegraphai_functions.py), но не был испытан за неименеием технических возможностей)

---

## 🤝 Контакты и вклад

Pull Request'ы приветствуются!
Если вы нашли баг — создайте issue.

Автор: [B3aRrrr](https://github.com/B3aRrrr)
