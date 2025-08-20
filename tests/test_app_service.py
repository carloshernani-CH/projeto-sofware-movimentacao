import pytest
from unittest.mock import MagicMock, patch
import requests
from app_service import (
    validar_campos,
    calcular_valor,
    criar_objeto_movimentacao,
)

def test_validar_campos_completos():
    data = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    assert validar_campos(data) is None

@pytest.mark.parametrize("faltando", ["cpf_comprador", "cpf_vendedor", "ticker", "quantidade"])
def test_validar_campos_faltando(faltando):
    base = {
        "cpf_comprador": "123",
        "cpf_vendedor": "456",
        "ticker": "PETR4",
        "quantidade": 10
    }
    base.pop(faltando)
    erro = validar_campos(base)
    assert erro is not None
    assert faltando in erro

@patch("app_service.requests.get")
def test_calcular_valor_sucesso(mock_get):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"lastValue": 13.5}
    mock_get.return_value = resp

    total, erro = calcular_valor("PETR4", 2)
    assert erro is None
    assert total == pytest.approx(27.0)

@patch("app_service.requests.get")
def test_calcular_valor_nao_200(mock_get):
    resp = MagicMock()
    resp.status_code = 404
    mock_get.return_value = resp

    total, erro = calcular_valor("XXXX", 5)
    assert total is None
    assert "Erro ao buscar ticker" in erro

@patch("app_service.requests.get", side_effect=requests.RequestException("boom"))
def test_calcular_valor_excecao(_mock_get):
    total, erro = calcular_valor("ABCD", 1)
    assert total is None
    assert "Erro de conexão" in erro

def test_criar_objeto_movimentacao():
    data = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "VALE3",
        "quantidade": 3
    }
    obj = criar_objeto_movimentacao(data, 99.9)
    assert obj == {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "VALE3",
        "quantidade": 3,
        "valor_movimentacao": 99.9,
    }
