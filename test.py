from scrapegraphai.graphs import SmartScraperGraph

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
            "model": "owl/t-lite",#"ollama/llama3.2",
            # "model_tokens": 8192
        },
    "verbose": True,
    "headless": True,
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="Extract full news content",
    source="https://ria.ru/20250512/dnr-2016505307.html",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()

import json
print(json.dumps(result, indent=4))