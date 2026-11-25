import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")
SITE = os.getenv("SITE_URL")
EMAIL = os.getenv("QA_EMAIL")
SENHA = os.getenv("QA_SENHA")


def entrar(page, email=EMAIL, senha=SENHA):
    """Abre o sistema de teste e faz login pela tela."""
    page.goto(SITE)
    page.fill("#lu", email)
    page.fill("#lp", senha)
    page.click("#lb")


@pytest.fixture
def api():
    """Endereço e cabeçalho básico, sem login."""
    return {"url": URL, "headers": {"apikey": KEY, "Content-Type": "application/json"}}


@pytest.fixture
def token(api):
    """Faz login pela API com o usuário de teste e devolve o token de acesso."""
    resposta = requests.post(
        f"{URL}/auth/v1/token?grant_type=password",
        headers=api["headers"],
        json={"email": EMAIL, "password": SENHA},
    )
    assert resposta.status_code == 200, "Login do usuário de teste falhou"
    return resposta.json()["access_token"]


@pytest.fixture
def dados_qa(api, token):
    """Cria um cliente com veículo e contrato ativo antes do teste e apaga tudo no final."""
    cabecalho = {**api["headers"], "Authorization": f"Bearer {token}"}
    registros = [
        {"id": "planos:qa-plano", "tipo": "planos", "dados": {
            "id": "qa-plano", "nome": "Plano QA", "valor": 99.9,
            "descricao": "Plano de teste", "status": "Ativo"}},
        {"id": "clientes:qa-cliente", "tipo": "clientes", "dados": {
            "id": "qa-cliente", "nome": "Cliente QA Teste", "tipo": "PF",
            "documento": "000.000.000-00", "telefone": "(98) 90000-0000",
            "email": "cliente.qa@exemplo.com", "endereco": "Rua de Teste, 1",
            "cidade": "São Luís - MA", "status": "Ativo"}},
        {"id": "veiculos:qa-veiculo", "tipo": "veiculos", "dados": {
            "id": "qa-veiculo", "clienteId": "qa-cliente", "placa": "QAA0A00",
            "marca": "Fiat", "modelo": "Uno", "ano": 2020, "cor": "Branco"}},
        {"id": "contratos:qa-contrato", "tipo": "contratos", "dados": {
            "id": "qa-contrato", "numero": "QA-0001", "clienteId": "qa-cliente",
            "veiculoId": "qa-veiculo", "planoId": "qa-plano", "inicio": "2026-01-10",
            "diaVencimento": 10, "status": "Ativo", "adesao": 0, "docStatus": "Assinado"}},
    ]
    apagar_dados_qa(cabecalho)
    resposta = requests.post(
        f"{URL}/rest/v1/registros",
        headers={**cabecalho, "Prefer": "resolution=merge-duplicates"},
        json=registros,
    )
    assert resposta.status_code in (200, 201), resposta.text
    yield
    apagar_dados_qa(cabecalho)


def apagar_dados_qa(cabecalho):
    """Apaga os dados de teste e as mensalidades geradas para o contrato de teste."""
    requests.delete(f"{URL}/rest/v1/registros?id=like.*:qa-*", headers=cabecalho)
    requests.delete(
        f"{URL}/rest/v1/registros?tipo=eq.mensalidades&dados->>contratoId=eq.qa-contrato",
        headers=cabecalho,
    )