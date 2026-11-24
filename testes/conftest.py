import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")


@pytest.fixture
def api():
    """Endereço e cabeçalho básico, sem login."""
    return {"url": URL, "headers": {"apikey": KEY, "Content-Type": "application/json"}}


@pytest.fixture
def token(api):
    """Faz login com o usuário de teste e devolve o token de acesso."""
    resposta = requests.post(
        f"{URL}/auth/v1/token?grant_type=password",
        headers=api["headers"],
        json={"email": os.getenv("QA_EMAIL"), "password": os.getenv("QA_SENHA")},
    )
    assert resposta.status_code == 200, "Login do usuário de teste falhou"
    return resposta.json()["access_token"]