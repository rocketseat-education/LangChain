from pathlib import Path

import weaviate
from langchain.embeddings import init_embeddings
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate.vectorstores import WeaviateVectorStore
from weaviate.classes.init import Auth

from src.config import EMBEDDINGS_ID, WEAVIATE_API_KEY, WEAVIATE_INDEX, WEAVIATE_URL

_DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
_client = None      # conexão com o Weaviate (singleton lazy)
_retriever = None   # retriever sobre a coleção (singleton lazy)


def _carregar_documentos() -> list[Document]:
    """Carrega docs/ (.md e .txt) com pathlib puro — sem libs deprecadas.

    Substitui o DirectoryLoader/TextLoader do langchain_community, que além
    de deprecado ainda puxava a dependência pesada 'unstructured'.
    """
    documentos: list[Document] = []
    for caminho in sorted(_DOCS_DIR.rglob("*")):
        if caminho.suffix.lower() not in (".md", ".txt"):
            continue
        documentos.append(
            Document(
                page_content=caminho.read_text(encoding="utf-8"),
                metadata={
                    "source": str(caminho),      # caminho completo, como o loader fazia
                    "fonte": caminho.name,        # só o nome do arquivo, usado na resposta
                },
            )
        )
    return documentos


def _get_client():
    """Conecta ao Weaviate Cloud uma vez (singleton lazy)."""
    global _client
    if _client is None:
        _client = weaviate.connect_to_weaviate_cloud(
            cluster_url=WEAVIATE_URL,
            auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        )
    return _client


def importar_documentos() -> int:
    """ESCRITA: lê docs/, quebra em chunks, vetoriza e GRAVA no Weaviate. Rode UMA vez."""
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(
        _carregar_documentos()
    )
    embeddings = init_embeddings(EMBEDDINGS_ID)
    WeaviateVectorStore.from_documents(       # cria a coleção, vetoriza e sobe os chunks
        chunks, embeddings, client=_get_client(),
        index_name=WEAVIATE_INDEX, text_key="text",
    )
    return len(_carregar_documentos())


def get_retriever():
    """LEITURA: retriever sobre a coleção JÁ importada (singleton lazy)."""
    global _retriever
    if _retriever is None:
        embeddings = init_embeddings(EMBEDDINGS_ID)   # vetoriza a PERGUNTA na busca
        vector_store = WeaviateVectorStore(
            client=_get_client(), index_name=WEAVIATE_INDEX,
            text_key="text", embedding=embeddings,
        )
        _retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    return _retriever


def warmup(importar: bool = False) -> int:
    """No startup: importa (se importar=True) ou só conecta na base já existente."""
    if importar:
        return importar_documentos()
    get_retriever()
    return len(_carregar_documentos())


@tool
def buscar_contexto(pergunta: str) -> str:
    """Busca trechos relevantes na base de conhecimento INTERNA da empresa.

    Use para assuntos internos (políticas, planos, FAQ) — o que a web não conhece.

    Args:
        pergunta: o que se quer saber, em linguagem natural.
    """
    docs = get_retriever().invoke(pergunta)
    if not docs:
        return "Nenhum trecho relevante encontrado nos documentos internos."
    return "\n\n".join(f"[{d.metadata.get('fonte', '?')}] {d.page_content}" for d in docs)