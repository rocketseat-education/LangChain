# 🔎 Assistente de Pesquisa (versão completa)

Assistente de linha de comando construído com **LangChain v1** + **LangGraph**. Ele é um **agente** que decide sozinho qual ferramenta usar para responder e devolve a resposta em um **formato estruturado** (título, pontos e fontes).

Este é o projeto final do **Módulo 2** do curso — a versão de referência, com RAG persistente, saída estruturada, memória de conversa e testes.

## ✨ O que ele faz

O agente tem **três ferramentas** e escolhe a mais adequada a cada pergunta:

| Ferramenta          | Para que serve                                                        | Como funciona                       |
| ------------------- | --------------------------------------------------------------------- | ----------------------------------- |
| `buscar_contexto`   | Assuntos **internos** (políticas, planos, FAQ) — a base da empresa    | RAG sobre o **Weaviate Cloud**      |
| `busca_web`         | Assuntos **gerais/atuais** que a base interna não cobre               | **Tavily** (busca na web)           |
| `previsao_tempo`    | Previsão do tempo de uma cidade                                       | Requisição HTTP (`requests`)        |

Outros recursos:

- **Saída estruturada** (`ResumoPesquisa`): sempre um título, de 3 a 5 pontos e as fontes usadas.
- **Memória de conversa**: mantém o contexto do diálogo (via `thread_id` do LangGraph).
- **RAG persistente**: os documentos de `docs/` viram vetores gravados no **Weaviate Cloud** — você importa **uma vez** e depois só consulta.

## 📁 Estrutura

```
assistente-pesquisa-completo/
├── docs/                 # base de conhecimento interna (.md) — vira o RAG
│   ├── faq-suporte.md
│   ├── planos-precos.md
│   └── politica-ferias.md
├── src/
│   ├── main.py           # ponto de entrada (CLI): conecta, importa e conversa
│   ├── assistente.py     # cria o agente (create_agent) com tools + saída estruturada
│   ├── tools.py          # as 3 ferramentas: previsao_tempo, busca_web, buscar_contexto
│   ├── rag.py            # carga de docs/ (pathlib) + Weaviate + retriever
│   ├── prompts.py        # SYSTEM_PROMPT do agente
│   ├── schemas.py        # ResumoPesquisa (formato da resposta)
│   ├── config.py         # lê o .env e valida as chaves obrigatórias
│   └── llm.py
├── tests/                # testes com pytest
├── requirements.txt
└── .env.example          # modelo das variáveis de ambiente
```

## ✅ Pré-requisitos

- **Python 3.10+** (recomendado 3.11 ou superior).
- Uma conta na **OpenAI** (modelo + embeddings) — [platform.openai.com](https://platform.openai.com/api-keys).
- Uma conta na **Tavily** (busca na web) — [tavily.com](https://www.tavily.com/).
- Um cluster no **Weaviate Cloud** (vector store do RAG) — [console.weaviate.cloud](https://console.weaviate.cloud/).

## 🚀 Instalação

Rode todos os comandos **a partir da raiz do projeto** (`assistente-pesquisa-completo/`).

**1. Crie e ative um ambiente virtual**

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

**2. Instale as dependências**

```bash
pip install -U -r requirements.txt
```

**3. Configure as variáveis de ambiente**

Copie o modelo e preencha suas chaves:

```bash
cp .env.example .env
```

Edite o `.env`:

```ini
# Obrigatórias
OPENAI_API_KEY=sk-...          # modelo + embeddings
TAVILY_API_KEY=tvly-...        # busca na web
WEAVIATE_URL=https://...       # URL do seu cluster Weaviate Cloud
WEAVIATE_API_KEY=...           # API key do cluster

# Opcionais (têm padrão sensato)
MODEL_ID=openai:gpt-4o-mini            # modelo base
AGENT_MODEL_ID=openai:gpt-4o           # modelo do agente
EMBEDDINGS_ID=openai:text-embedding-3-small
WEAVIATE_INDEX=AssistenteDocs          # nome da coleção no Weaviate
```

> O `main.py` valida as chaves obrigatórias no início e avisa se faltar alguma — então dá pra corrigir cedo, sem quebrar no meio.

## ▶️ Como executar

O projeto roda como **módulo** (por causa dos imports `from src...`), sempre da raiz:

**1. Importe os documentos para o Weaviate (só na primeira vez)**

Lê `docs/`, quebra em chunks, gera os embeddings e grava no seu cluster:

```bash
python -m src.main --import
```

**2. Depois, é só conversar** (usa os dados já importados)

```bash
python -m src.main
```

Você entra num loop de perguntas. Digite `sair` (ou `exit`, ou linha vazia) para encerrar:

```
🔎 Assistente (digite 'sair' para encerrar)

> Qual é a política de férias da empresa?

📌 Política de Férias
  • ...
  • ...
Fontes: politica-ferias.md
```

### Flags disponíveis

| Comando                      | O que faz                                                        |
| ---------------------------- | ---------------------------------------------------------------- |
| `python -m src.main`         | Conversa usando os dados **já importados** no Weaviate.          |
| `python -m src.main --import`| **Importa** `docs/` para o Weaviate e depois inicia a conversa.  |
| `python -m src.main --debug` | Mostra o **passo a passo** do agente (cada chamada de ferramenta).|

> Rode `--import` novamente sempre que **mudar os arquivos** em `docs/`.

## 🧪 Testes

```bash
pytest
```

Os testes são **offline** (a conexão com o Weaviate é *lazy*, só acontece ao importar/consultar de verdade), então rodam sem rede.

## 🛠️ Personalizando

- **Trocar de modelo**: ajuste `MODEL_ID` / `AGENT_MODEL_ID` no `.env` (o ID muda, a API do LangChain não).
- **Usar seus próprios documentos**: troque os `.md` em `docs/` pelos seus (`.md` ou `.txt`) e rode `python -m src.main --import`.
- **Ajustar o RAG**: em `src/rag.py`, mude `chunk_size` / `chunk_overlap` (splitter) ou `k` (quantidade de trechos recuperados).

## 📝 Notas técnicas

- A carga de `docs/` usa **`pathlib` puro** (não o `DirectoryLoader` do `langchain-community`, que está em [*sunset*](https://github.com/langchain-ai/langchain-community/issues/674)) — sem dependências deprecadas.
- O vector store é **persistente** no Weaviate Cloud: `--import` grava uma vez; as execuções seguintes apenas **consultam**.
- A memória de conversa usa `InMemorySaver` do LangGraph (vive só durante a execução).
