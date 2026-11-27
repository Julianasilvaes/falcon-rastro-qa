import re
from playwright.sync_api import Page, expect
from conftest import entrar


def valor_em_reais(texto):
    """Transforma um texto como 'R$ 1.234,56' no número 1234.56."""
    achado = re.search(r"R\$\s*([\d.]+,\d{2})", texto)
    assert achado, f"Nenhum valor em reais encontrado em: {texto}"
    return float(achado.group(1).replace(".", "").replace(",", "."))


def recebido_no_mes(page: Page):
    page.click('a[href="#painel"]')
    kpi = page.locator(".kpi", has_text="Recebido no mês")
    expect(kpi).to_be_visible()
    return valor_em_reais(kpi.inner_text())


def test_gerar_e_receber_mensalidade(dados_qa, page: Page):
    entrar(page)
    expect(page.locator("main h1")).to_have_text(re.compile("Bom dia|Boa tarde|Boa noite"))

    # guardar quanto já tinha entrado no mês antes do teste
    antes = recebido_no_mes(page)

    # gerar as mensalidades do mês atual
    page.click('a[href="#mensalidades"]')
    page.click("[data-act=gerar]")
    page.click("#okb")
    expect(page.get_by_text(re.compile(r"\d+ mensalidade\(s\) gerada\(s\)"))).to_be_visible()

    # registrar o pagamento da mensalidade do cliente de teste
    linha = page.locator("tr", has_text="Cliente QA Teste")
    expect(linha).to_be_visible()
    linha.locator("[data-act=receber]").click()
    recebido = valor_em_reais(page.locator("#rfTotal").inner_text())
    page.click("#rf .btn:not(.ghost)")
    expect(page.get_by_text("Pagamento registrado")).to_be_visible()

    # o painel tem que somar exatamente o valor recebido
    depois = recebido_no_mes(page)
    assert round(depois - antes, 2) == round(recebido, 2)