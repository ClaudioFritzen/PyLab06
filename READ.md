
dia 19/04/23 Alteração proposta sera que depois de logado não posso mais ir pra tela 
de login e cadastro pela url

Para solucionar esse problema iremos importar as autenticações que ja vem pronto com o django

from django.contrib.auth import autenticate, login, logout

iremos começar pelo cadastro

entao logo apos a declaração da função

def cadastro(request):

    ## aqui faremos a validação para ver se o usuario já está logado.

    if request.user.is_authenticated:
        #### mensagens de alertas
        return redirect('eventos/novo_evento')

### para o login é praticamente a mesma coisa

def login(request):

    if request.user.is_authenticated:
    ## mensagens de erro
        return redirect('eventos/novo_evento')

