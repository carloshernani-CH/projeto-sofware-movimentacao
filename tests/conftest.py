import pytest
from app import app as flask_app
import app as app_module

@pytest.fixture(autouse=True)
def reset_state(monkeypatch):
    # zera o "banco" entre testes
    monkeypatch.setattr(app_module, "movimentacoes", [], raising=True)
    yield

@pytest.fixture
def client():
    flask_app.testing = True
    return flask_app.test_client()
