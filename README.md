# Falcon Rastro QA

![Testes automatizados](https://github.com/Julianasilvaes/falcon-rastro-qa/actions/workflows/testes.yml/badge.svg)

Testes automatizados do sistema de gestão da Falcon Rastro, empresa de rastreamento veicular de São Luís (MA). O sistema está em uso real: controla clientes, veículos, rastreadores, contratos, agenda de instalação e cobrança de mensalidades.

Os testes rodam no ambiente de homologação ([teste.falconrastro.pages.dev](https://teste.falconrastro.pages.dev)), que tem banco de dados e usuário próprios, separados da produção.

## O que é testado

| Arquivo | Tipo | O que valida |
|---|---|---|
| `test_seguranca_api.py` | API | Sem login não é possível ler nem gravar dados; o cadastro público está desligado; senha errada é recusada; com login válido a leitura funciona |
| `test_login.py` | Interface (E2E) | Login com dados corretos, login com senha errada e saída do sistema |
| `test_mensalidades.py` | Interface (E2E) | Gera as mensalidades do mês, registra um pagamento e confere se o painel financeiro soma exatamente o valor recebido |

Cada teste que precisa de dados cria os próprios registros antes de rodar (cliente, veículo e contrato com prefixo `qa-`) e apaga tudo ao terminar, sem mexer nos outros dados do ambiente.

## Ferramentas

- Python, pytest e Playwright
- requests para os testes de API
- GitHub Actions: os testes rodam a cada envio para a main e de segunda a sexta às 8h, para avisar se a homologação quebrou mesmo sem mudança no código
- Credenciais guardadas em GitHub Secrets e em `.env` local, fora do repositório

O sistema testado usa Supabase (PostgreSQL, autenticação e Row Level Security) e é publicado no Cloudflare Pages, com um ambiente de produção e outro de homologação.

## Documentação

- [Plano de teste](testes/docs/plano_de_teste.md)
- Cenários em Gherkin: [login](testes/docs/cenarios/login.feature) e [mensalidades](testes/docs/cenarios/mensalidades.feature)

## Bugs encontrados

Os testes e a validação manual de todas as telas encontraram 4 bugs de gravidade alta, 9 de gravidade média e 4 erros de português, todos corrigidos. Dois deles:

**Pagamento sumia da tela depois de registrado.** A atualização em tempo real do banco devolvia o mesmo registro com os campos em outra ordem, o sistema entendia isso como uma versão diferente e sobrescrevia o pagamento recém-salvo. A correção passou a comparar os registros pelo conteúdo, e não pela ordem dos campos.

**Alterações perdidas com a sessão expirada.** Quando o login expirava, o banco recusava a gravação, mas a tela mostrava a mensagem de sucesso. A correção passou a identificar a recusa, avisar que a alteração não foi salva e levar o usuário de volta para o login.

A integração contínua também mostrou uma fragilidade do próprio teste de mensalidades: ele esperava o banco vazio e falhou quando a homologação já tinha outros pagamentos no mês. O teste foi reescrito para comparar o painel antes e depois do pagamento.

## Como rodar no computador

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
pytest testes -v
```

Antes, crie um arquivo `.env` na raiz do projeto com as variáveis `SUPABASE_URL`, `SUPABASE_KEY`, `QA_EMAIL`, `QA_SENHA` e `SITE_URL`.

## Autora

Juliana Silva e Silva · [LinkedIn](https://www.linkedin.com/in/julianasilvaesilva)