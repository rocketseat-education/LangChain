from unittest.mock import Mock, patch

from langchain_core.documents import Document
from src.rag import buscar_contexto


def test_buscar_contexto_formata_os_trechos():
    docs = [
        Document(page_content="Você tem 30 dias de férias por ano.",
                 metadata={"fonte": "politica-ferias.md"}),
    ]
    retriever = Mock(); retriever.invoke.return_value = docs

    with patch("src.rag.get_retriever", return_value=retriever):
        saida = buscar_contexto.invoke({"pergunta": "quantos dias de férias eu tenho?"})

    assert "politica-ferias.md" in saida     # cita a fonte
    assert "30 dias" in saida                 # traz o conteúdo


def test_buscar_contexto_sem_resultados():
    retriever = Mock(); retriever.invoke.return_value = []

    with patch("src.rag.get_retriever", return_value=retriever):
        saida = buscar_contexto.invoke({"pergunta": "algo que não existe na base"})

    assert "Nenhum trecho" in saida