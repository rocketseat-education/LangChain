from langchain.chat_models import init_chat_model
from src.config import validar_ambiente

from src.config import MODEL_ID


def get_model():
    """Instancia e devolve o chat model do projeto.

    Centraliza a criação do modelo em UM lugar: prompts, chains e
    agents das próximas aulas vão pedir o modelo a esta função, em
    vez de chamar init_chat_model espalhado pelo código.

    O ID vem do config (MODEL_ID), que por sua vez pode vir do .env —
    então trocar de modelo continua sendo mudança de uma linha só.
    """
    # init_chat_model entende a string "provedor:modelo".
    # Ex.: "openai:gpt-4o-mini" -> usa o pacote langchain-openai.
    return init_chat_model(MODEL_ID)

def testar_modelo() -> str:
    """Faz um invoke simples para confirmar que a comunicação funciona.

    Valida o ambiente antes (falha cedo, com mensagem clara, se faltar
    a chave) e devolve o texto da resposta do modelo.
    """
    # 1) Confere se as chaves obrigatórias existem (definido no config.py).
    validar_ambiente()

    # 2) Pede o modelo ao módulo central e faz uma pergunta simples.
    model = get_model()
    resposta = model.invoke("Diga apenas: 'Conexão com o modelo OK'.")

    # 3) Devolve o TEXTO (AIMessage.text), não o objeto inteiro.
    return resposta.text