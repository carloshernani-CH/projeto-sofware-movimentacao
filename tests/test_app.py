import json
import pytest
import app as app_module

def test_post_criar_movimentacao_sucesso(client, monkeypatch):
    # mocka validação (ok) e cálculo (ok)
    monkeypatch.setattr(app_module, "validar_campos", lambda d: None, raising=True)
    monkeypatch.setattr(app_module, "calcular_valor", lambda t,q: (30.0, None), raising=True)

    payload = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "PETR4",
        "quantidade": 2
    }
    resp = client.post("/movimentacoes", json=payload)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["valor_movimentacao"] == pytest.approx(30.0)
    assert len(app_module.movimentacoes) == 1

def test_post_criar_movimentacao_erro_validacao(client, monkeypatch):
    monkeypatch.setattr(app_module, "validar_campos", lambda d: "Campo obrigatório 'ticker' não informado", raising=True)
    resp = client.post("/movimentacoes", json={"foo": "bar"})
    assert resp.status_code == 400
    assert "erro" in resp.get_json()

def test_post_criar_movimentacao_erro_calculo(client, monkeypatch):
    monkeypatch.setattr(app_module, "validar_campos", lambda d: None, raising=True)
    monkeypatch.setattr(app_module, "calcular_valor", lambda t,q: (None, "Erro ao buscar ticker"), raising=True)

    payload = {
        "cpf_comprador": "111",
        "cpf_vendedor": "222",
        "ticker": "XXXX",
        "quantidade": 1
    }
    resp = client.post("/movimentacoes", json=payload)
    assert resp.status_code == 400
    assert "erro" in resp.get_json()

def test_get_listar_movimentacoes(client, monkeypatch):
    seed = [
        {"cpf_comprador": "1", "cpf_vendedor": "2", "ticker": "ABC1", "quantidade": 1, "valor_movimentacao": 10.0},
        {"cpf_comprador": "3", "cpf_vendedor": "4", "ticker": "DEF2", "quantidade": 2, "valor_movimentacao": 20.0},
    ]
    monkeypatch.setattr(app_module, "movimentacoes", seed, raising=True)
    resp = client.get("/movimentacoes")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body == seed
