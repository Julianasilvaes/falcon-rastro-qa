# language: pt
Funcionalidade: Cobrança de mensalidades
  Como responsável pelo financeiro
  Quero gerar e receber as mensalidades dos clientes
  Para controlar o que entrou no caixa do mês

  Contexto:
    Dado que estou logado no sistema
    E existe um cliente com veículo e contrato ativo

  Cenário: Gerar mensalidades do mês
    Quando gero as mensalidades do mês atual
    Então a mensalidade do cliente aparece como pendente

  Cenário: Registrar pagamento
    Dado que existe uma mensalidade pendente
    Quando registro o pagamento
    Então a mensalidade aparece como paga
    E o valor entra no recebido do mês, no painel
