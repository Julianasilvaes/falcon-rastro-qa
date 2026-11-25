import os
import re
from playwright.sync_api import Page, expect

SITE = os.getenv("SITE_URL")
EMAIL = os.getenv("QA_EMAIL")
SENHA = os.getenv("QA_SENHA")


def entrar(page: Page, email: str, senha: str):
    page.goto(SITE)
    page.fill("#lu", email)
    page.fill("#lp", senha)
    page.click("#lb")


def test_login_com_dados_corretos(page: Page):
    entrar(page, EMAIL, SENHA)
    expect(page.locator("#app")).to_be_visible()
    expect(page.locator("main h1")).to_have_text(re.compile("Bom dia|Boa tarde|Boa noite"))


def test_login_com_senha_errada(page: Page):
    entrar(page, EMAIL, "senha-errada-123")
    expect(page.locator("#lerr")).to_have_text("E-mail ou senha incorretos")
    expect(page.locator("#login")).to_be_visible()


def test_saida_do_sistema(page: Page):
    entrar(page, EMAIL, SENHA)
    expect(page.locator("#app")).to_be_visible()
    page.click("#logoutBtn")
    expect(page.locator("#login")).to_be_visible()