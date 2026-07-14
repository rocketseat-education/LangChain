from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

from src.config import AGENT_MODEL_ID   # modelo do agente (config/.env)
from src.prompts import SYSTEM_PROMPT    # papel do agente (prompts.py)
from src.tools import ferramentas       # tools do agente (tools.py)
from src.schemas import ResumoPesquisa   # ← NOVO

# Registra o tipo do response_format para o checkpointer poder desserializá-lo.
serde = JsonPlusSerializer(
    allowed_msgpack_modules=[("src.schemas", "ResumoPesquisa")]
)

@wrap_tool_call
def tratar_erro_de_tool(request, handler):
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"A ferramenta falhou: {e}. Responda com o que já tem — não repita a chamada.",
            tool_call_id=request.tool_call["id"],
        )

def criar_assistente():
    return create_agent(
        model=AGENT_MODEL_ID,
        tools=ferramentas,                        # ainda SEM ferramentas
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(serde=serde),    # <- memória de curto prazo (por thread_id)
        response_format=ResumoPesquisa,
        middleware=[tratar_erro_de_tool],
    )