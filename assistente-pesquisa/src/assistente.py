from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from src.config import AGENT_MODEL_ID   # modelo do agente (config/.env)
from src.prompts import SYSTEM_PROMPT    # papel do agente (prompts.py)


def criar_assistente():
    return create_agent(
        model=AGENT_MODEL_ID,
        tools=[],                        # ainda SEM ferramentas
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),    # <- memória de curto prazo (por thread_id)
    )