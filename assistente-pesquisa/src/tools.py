import requests
from langchain.tools import tool
from langchain_tavily import TavilySearch

# Códigos de tempo (padrão WMO) -> descrição (os mais comuns).
_CODIGOS_TEMPO = {
    0: "céu limpo", 1: "predominantemente limpo", 2: "parcialmente nublado",
    3: "nublado", 45: "névoa", 61: "chuva leve", 63: "chuva moderada",
    65: "chuva forte", 80: "pancadas de chuva", 95: "trovoada",
    # ... demais códigos WMO
}

busca_web = TavilySearch(max_results=5)

@tool
def previsao_tempo(local: str) -> str:
    """Consulta a previsão do tempo ATUAL de qualquer lugar do mundo.

    Use quando o usuário perguntar sobre clima, temperatura ou condições do
    tempo de uma cidade, região ou país.

    Args:
        local: nome do lugar (ex.: "São Paulo", "Tokyo", "Paris, França").
    """
    # 1) GEOCODING: nome do local -> latitude/longitude.
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": local, "count": 1, "language": "pt", "format": "json"},
        timeout=10,
    ).json()
    resultados = geo.get("results")
    if not resultados:
        return f"Não encontrei o local '{local}'. Tente ser mais específico."

    lugar = resultados[0]
    lat, lon = lugar["latitude"], lugar["longitude"]
    nome, pais = lugar["name"], lugar.get("country", "")

    # 2) FORECAST: clima atual naquela coordenada.
    atual = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat, "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        },
        timeout=10,
    ).json()["current"]
    condicao = _CODIGOS_TEMPO.get(atual["weather_code"], "condição desconhecida")

    return (
        f"Tempo agora em {nome}, {pais}: {condicao}, "
        f"{atual['temperature_2m']}°C, umidade {atual['relative_humidity_2m']}%, "
        f"vento {atual['wind_speed_10m']} km/h."
    )


# Lista de tools do projeto — o agente recebe todas de uma vez (vai crescer).
ferramentas = [previsao_tempo, busca_web]