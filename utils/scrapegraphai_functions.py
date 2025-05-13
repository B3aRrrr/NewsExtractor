from scrapegraphai.graphs import SmartScraperGraph
import json

def extract_article_text(url: str) -> dict:
    # Define the configuration for the scraping pipeline
    graph_config = {
        "llm": {
            "model": "ollama/llama3.2",
            "model_tokens": 8192
        },
        "verbose": True,
        "headless": False,
    }

    # Create the SmartScraperGraph instance
    smart_scraper_graph = SmartScraperGraph(
        prompt="Extract useful information from the webpage, including a description of what the company does, founders and social media links",
        source=url,
        config=graph_config
    )

    # Run the pipeline
    result = smart_scraper_graph.run()

    return json.dumps(result, indent=4)

# === Пример использования ===
if __name__ == "__main__":
    url = "https://ria.ru/20250512/dnr-2016505307.html"  # Пример: замени на нужный URL
    article_text = extract_article_text(url)
    print("=== Извлечённый текст (json) ===")
    print(article_text)
