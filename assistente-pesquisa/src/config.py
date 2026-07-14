import os
from dotenv import load_dotenv

# Carrega o .env UMA vez, no ponto central do projeto.
# (os demais módulos NÃO precisam chamar load_dotenv de novo)
load_dotenv()

# ID do modelo padrão — trocável em um só lugar (ou via .env).
# Lembre: o ID muda, mas a API do LangChain não.
MODEL_ID = os.getenv("MODEL_ID", "openai:gpt-4o-mini")
AGENT_MODEL_ID = os.getenv("AGENT_MODEL_ID", MODEL_ID)

EMBEDDINGS_ID = os.getenv("EMBEDDINGS_ID", "openai:text-embedding-3-small")

WEAVIATE_URL = os.getenv("WEAVIATE_URL", "")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")
WEAVIATE_INDEX = os.getenv("WEAVIATE_INDEX", "AssistenteDocs")   # nome da coleção

def validar_ambiente() -> None:
    """Confere se as chaves essenciais existem.

    Chamamos isso no início do main.py para falhar cedo, com uma
    mensagem clara, em vez de quebrar no meio da execução.
    """
    obrigatorias = (
        "OPENAI_API_KEY",    # modelo + embeddings
        "TAVILY_API_KEY",    # busca na web
        "WEAVIATE_URL",      # vector store persistente do RAG
        "WEAVIATE_API_KEY",
    )
    faltando = [nome for nome in obrigatorias if not os.getenv(nome)]
    if faltando:
        raise RuntimeError(
            "Defina no seu .env (veja o .env.example): " + ", ".join(faltando) + "."
        )