from pydantic import BaseModel, Field


class ResumoPesquisa(BaseModel):
    """Formato padrão da resposta do assistente."""
    titulo: str = Field(description="Um título curto para a resposta.")
    pontos: list[str] = Field(description="De 3 a 5 pontos principais.")
    fontes: list[str] = Field(
        default_factory=list, description="Fontes/URLs usadas, se houver."
    )