import os

basedir = os.path.abspath((os.path.dirname(__file__)))

class Config:
    DATASETS_FOLDER=os.path.join(basedir,'datasets')
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/115.0.0.0 Safari/537.36'
    }
    GRAPH_CONFIG = {
        "llm": {
            "model": "owl/t-lite",#"ollama/llama3.2",
            # "model_tokens": 8192
        },
        "verbose": True,
        "headless": True,
    }

config = {
    
    'default':Config
}