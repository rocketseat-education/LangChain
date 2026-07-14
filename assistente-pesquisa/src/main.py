from src.assistente import criar_assistente
from src.config import validar_ambiente


def main() -> None:
    # Falha cedo se faltar alguma chave obrigatória (Aula 2/3).
    try:
        validar_ambiente()
    except RuntimeError as e:
        print(f"⚠️  Configuração incompleta: {e}")
        return

    agente = criar_assistente()          # cria o agente UMA vez, fora do loop
    print("🔎 Assistente de Pesquisa (digite 'sair' para encerrar)\n")

    while True:
        pergunta = input("> ").strip()
        if pergunta.lower() in {"sair", "exit", ""}:
            print("Até a próxima! 👋")
            break
        try:
            resposta = agente.invoke(
                {"messages": [{"role": "user", "content": pergunta}]}
            )
            print(resposta["messages"][-1].content, "\n")
        except Exception as e:
            print(f"⚠️  Não consegui responder: {e}\n")


if __name__ == "__main__":
    main()