# main.py — rode a partir da raiz:
#   python main.py            # usa os dados JÁ importados no Weaviate
#   python main.py --import   # importa os documentos de docs/ e depois usa
#   python main.py --debug    # mostra o passo a passo do agente (chamadas de tools)
import argparse

from dotenv import load_dotenv

from src.assistente import criar_assistente
from src.config import validar_ambiente   # confere as chaves obrigatórias
from src.rag import warmup

load_dotenv()


def exibir(resumo):
    print(f"\n📌 {resumo.titulo}")
    for p in resumo.pontos:
        print(f"  • {p}")
    if resumo.fontes:
        print("Fontes:", ", ".join(resumo.fontes))


def main():
    parser = argparse.ArgumentParser(description="Assistente de Pesquisa (RAG no Weaviate).")
    parser.add_argument("--import", dest="importar", action="store_true",
                        help="Importa os documentos de docs/ para o Weaviate antes de iniciar.")
    parser.add_argument("--debug", action="store_true",
                        help="Mostra o passo a passo do agente (chamadas de ferramentas).")
    args = parser.parse_args()

    try:                              # falha cedo se faltar alguma chave (Aula 2/3)
        validar_ambiente()
    except RuntimeError as e:
        print(f"⚠️  Configuração incompleta: {e}")
        return

    print("📥 Importando..." if args.importar else "📚 Conectando à base...", end=" ", flush=True)
    try:
        n = warmup(importar=args.importar)          # importa (--import) ou só conecta
        print(f"{n} documento(s).")
    except Exception as e:
        print(f"pulado ({e}).")

    agente = criar_assistente()
    # thread_id = conversa contínua; recursion_limit = teto de passos (anti-loop, sem middleware)
    config = {"configurable": {"thread_id": "cli-1"}, "recursion_limit": 12}
    print("\n🔎 Assistente (digite 'sair' para encerrar)\n")

    while True:
        pergunta = input("> ").strip()
        if pergunta.lower() in {"sair", "exit", ""}:
            break
        try:
            estado = None
            for chunk in agente.stream(
                {"messages": [{"role": "user", "content": pergunta}]},
                config, stream_mode="values",
            ):
                if args.debug:                       # só com --debug: mostra cada passo
                    chunk["messages"][-1].pretty_print()
                estado = chunk
            exibir(estado["structured_response"])
        except Exception as e:
            print(f"⚠️ Não consegui responder: {e}")


if __name__ == "__main__":
    main()