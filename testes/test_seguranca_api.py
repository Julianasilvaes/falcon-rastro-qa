import requests


def test_sem_login_nao_le_registros(api):
    resposta = requests.get(f"{api['url']}/rest/v1/registros?select=*", headers=api["headers"])
    assert resposta.status_code in (401, 403) or resposta.json() == []


def test_sem_login_nao_grava_registros(api):
    novo = {"id": "teste:invasor", "tipo": "clientes", "dados": {"nome": "Invasor"}}
    resposta = requests.post(f"{api['url']}/rest/v1/registros", headers=api["headers"], json=novo)
    assert resposta.status_code in (401, 403)


def test_cadastro_publico_esta_desligado(api):
    resposta = requests.post(
        f"{api['url']}/auth/v1/signup",
        headers=api["headers"],
        json={"email": "intruso@exemplo.com", "password": "Senha12345"},
    )
    assert resposta.status_code >= 400


def test_login_com_senha_errada_e_recusado(api):
    resposta = requests.post(
        f"{api['url']}/auth/v1/token?grant_type=password",
        headers=api["headers"],
        json={"email": "qa@falconrastro.teste", "password": "senha-errada-123"},
    )
    assert resposta.status_code == 400


def test_com_login_valido_consegue_ler(api, token):
    cabecalho = {**api["headers"], "Authorization": f"Bearer {token}"}
    resposta = requests.get(f"{api['url']}/rest/v1/registros?select=*", headers=cabecalho)
    assert resposta.status_code == 200