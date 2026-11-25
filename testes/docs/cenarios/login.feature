# language: pt
Funcionalidade: Acesso ao sistema
  Como membro da equipe da Falcon Rastro
  Quero entrar no sistema com meu e-mail e senha
  Para gerenciar clientes, contratos e cobranças

  Cenário: Login com dados corretos
    Dado que estou na tela de login
    Quando informo e-mail e senha válidos
    E clico em "Entrar"
    Então vejo o painel com a saudação do dia

  Cenário: Login com senha errada
    Dado que estou na tela de login
    Quando informo um e-mail válido e uma senha errada
    E clico em "Entrar"
    Então vejo a mensagem "E-mail ou senha incorretos"
    E continuo na tela de login

  Cenário: Saída do sistema
    Dado que estou logado no sistema
    Quando clico em "Sair do sistema"
    Então volto para a tela de login