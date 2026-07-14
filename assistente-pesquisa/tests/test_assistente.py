from unittest.mock import patch

from src.schemas import ResumoPesquisa
from src.tools import ferramentas
import src.assistente as assistente


def test_resumo_pesquisa_valida_e_tem_default():
    r = ResumoPesquisa(titulo="Resumo", pontos=["a", "b", "c"])
    assert r.titulo == "Resumo"
    assert len(r.pontos) == 3
    assert r.fontes == []          # default_factory=list


def test_criar_assistente_monta_com_as_pecas_certas():
    with patch("src.assistente.create_agent") as mock_create:
        assistente.criar_assistente()

    mock_create.assert_called_once()
    kwargs = mock_create.call_args.kwargs
    assert kwargs["tools"] is ferramentas               # recebe as 3 tools
    assert kwargs["response_format"] is ResumoPesquisa  # saída estruturada
    assert kwargs["checkpointer"] is not None           # memória ligada