from src.config import MODEL_ID
from src.llm import testar_modelo

def main() -> None:
    print("Assistente de Pesquisa e Resumo — testando o modelo de IA")
    print(f"Modelo configurado: {MODEL_ID}\n")

    # Trata problemas de configuração com uma mensagem amigável.
    try:
        resposta = testar_modelo()
    except RuntimeError as e:
        # Ex.: chave ausente — validar_ambiente() levanta RuntimeError.
        print(f"⚠️  Configuração incompleta: {e}")
        return

    print("Resposta do modelo:")
    print(resposta)
    print("\n✅ Integração com o modelo funcionando! Próximo: o agente base (Aula 4).")

if __name__ == "__main__":
    main()