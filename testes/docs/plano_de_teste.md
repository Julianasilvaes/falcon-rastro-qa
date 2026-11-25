# Plano de teste: Sistema de Gestão Falcon Rastro

## Objetivo
Verificar se o sistema de gestão da Falcon Rastro, que está em uso na operação da empresa, funciona corretamente nas rotinas de cadastro, cobrança e contratos, e se os dados de clientes e do financeiro ficam bloqueados para quem não tem login.

## Sistema testado
Aplicação web de página única, publicada no Cloudflare Pages, com banco de dados e autenticação no Supabase. Os testes rodam em um ambiente separado, com banco próprio, para que nenhum dado real da empresa seja criado, alterado ou apagado durante a execução.

## Escopo
| Módulo                                  | Tipo de teste                     | Prioridade |
|-----------------------------------------|-----------------------------------|------------|
| Segurança da API                        | Automatizado (pytest e requests)  | Alta       |
| Login e recuperação de senha            | Automatizado (Playwright)         | Alta       |
| Clientes e veículos                     | Automatizado (Playwright)         | Alta       | 
| Contratos                               | Automatizado (Playwright)         | Alta       |
| Mensalidades e inadimplência            | Automatizado (Playwright)         | Alta       |
| Despesas, fluxo de caixa e relatórios   | Automatizado (Playwright)         | Média      |
| Agenda, técnicos, planos e rastreadores | Manual exploratório               | Média      |
| Uso em celular                          | Manual exploratório               | Média      |

## Fora do escopo
O envio real de mensagens pelo WhatsApp e o recebimento real por Pix ficam fora deste plano, porque dependem de serviços externos e movimentam dinheiro de verdade. Nesses pontos, os testes verificam só se a mensagem e o código Pix são gerados com os dados corretos.

## Riscos
Um erro nos valores das mensalidades ou do fluxo de caixa afeta diretamente a cobrança dos clientes e o controle financeiro da empresa. Uma falha de permissão no banco exporia dados pessoais de clientes, o que vai contra a LGPD, e uma falha no salvamento faria a equipe perder cadastros feitos durante o dia.

## Ferramentas
Python, pytest, requests, Playwright e GitHub Actions.

## Critério de aprovação
Uma nova versão só é publicada quando todos os testes de prioridade alta passam.