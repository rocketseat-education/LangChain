from unittest.mock import Mock, patch

from src.tools import previsao_tempo, busca_web, ferramentas
from src.rag import buscar_contexto


def test_ferramentas_tem_as_tres():
    assert previsao_tempo in ferramentas
    assert busca_web in ferramentas
    assert buscar_contexto in ferramentas


def test_previsao_tempo_com_mock():
    # A tool faz DUAS chamadas HTTP: geocoding e forecast.
    geo = Mock(); geo.json.return_value = {"results": [
        {"latitude": -8.0, "longitude": -34.9, "name": "Recife", "country": "Brasil"}]}
    fc = Mock(); fc.json.return_value = {"current": {
        "temperature_2m": 29.0, "relative_humidity_2m": 70,
        "wind_speed_10m": 12.0, "weather_code": 0}}

    with patch("src.tools.requests.get", side_effect=[geo, fc]) as mock_get:
        saida = previsao_tempo.invoke({"local": "Recife"})

    assert mock_get.call_count == 2
    assert "Recife" in saida and "céu limpo" in saida


def test_previsao_tempo_local_nao_encontrado():
    # Geocoding sem resultados -> mensagem amigável, SEM 2ª chamada.
    geo = Mock(); geo.json.return_value = {"results": []}
    with patch("src.tools.requests.get", return_value=geo):
        saida = previsao_tempo.invoke({"local": "Cidade Inexistente XYZ"})
    assert "Não encontrei" in saida