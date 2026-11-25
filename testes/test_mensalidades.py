import re
from playwright.sync_api import Page, expect
from conftest import entrar


def test_gerar_e_receber_mensalidade(dados_qa, page: Page):
    entrar(page)
    expect(page.locator("main h1")).to_have_text(re.compile("Bom dia|Boa tarde|Boa noite"))

    # gerar as mensalidades do mês atual
    page.click('a[href="#mensalidades"]')
    page.click("[data-act=gerar]")
    page.click("#okb")
    expect(page.get_by_text("1 mensalidade(s) gerada(s)")).to_be_visible()
    expect(page.locator("main")).to_contain_text("Cliente QA Teste")

    # registrar o pagamento
    page.locator("[data-act=receber]").first.click()
    page.click("#rf .btn:not(.ghost)")
    expect(page.get_by_text("Pagamento registrado")).to_be_visible()

    # conferir se o valor entrou no painel
    page.click('a[href="#painel"]')
    expect(page.locator(".kpi", has_text="Recebido no mês")).to_contain_text("R$ 99,90")