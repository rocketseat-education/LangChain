from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from src.config import AGENT_MODEL_ID   # modelo do agente (config/.env)
from src.prompts import SYSTEM_PROMPT    # papel do agente (prompts.py)
from src.tools import ferramentas       # tools do agente (tools.py)
from src.schemas import ResumoPesquisa   # ← NOVO

# Registra o tipo do response_format para o checkpointer poder desserializá-lo.
serde = JsonPlusSerializer(
    allowed_msgpack_modules=[("src.schemas", "ResumoPesquisa")]
)

def criar_assistente():
    return create_agent(
        model=AGENT_MODEL_ID,
        tools=ferramentas,                        # ainda SEM ferramentas
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(serde=serde),    # <- memória de curto prazo (por thread_id)
        response_format=ResumoPesquisa,
    )