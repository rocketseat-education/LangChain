import os

# Chaves fictícias: permitem IMPORTAR os módulos offline.
# Como tudo que usa rede é mockado, elas nunca são de fato usadas.
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("TAVILY_API_KEY", "test-key")
os.environ.setdefault("WEAVIATE_URL", "http://localhost:8080")
os.environ.setdefault("WEAVIATE_API_KEY", "test-key")