from src.config import MODEL_ID, validar_ambiente

def main() -> None:
    # 1) Falha cedo se faltar configuração (ex.: a chave da OpenAI).
    validar_ambiente()

    # 2) Por enquanto, só confirmamos que o projeto está de pé.
    print("Assistente de Pesquisa e Resumo — projeto inicializado ✅")
    print(f"Modelo configurado: {MODEL_ID}")
    print("Próximo passo: conectar o modelo de IA (Aula 3).")


# Permite rodar com:  python -m src.main
if __name__ == "__main__":
    main()
