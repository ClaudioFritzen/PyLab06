
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

    ## Atenticação de ususario
    if request.user.is_authenticated:
        ## mensagem de alerta
        messages.add_message(request, constants.WARNING, 'Não é possivél acessar essa URL logado.')
        return redirect('/eventos/novo_evento/')

## Validação para o tamanho da img
 # tamanho da img que pode ser recebida
        if logo.size > 100_000_000:
            messages.add_message(
                request,
                constants.ERROR,
                'A logo da empresa deve ter menos de 10MB',
            )
            return redirect('/home/nova_empresa')

#### tratamentos de erros na hora de cadastrar um evento.
 
# Primeiro erro que acontece quando tentamos cadastrar um evento vazio.

Para tratarmos esse erro faremos o seguinto.
Uma validação contando os caracteres dos campos.

erro apresentado de inicio foi sobre a data
para tentar fazer alguma validação
 tipo de data_inicial for igual a vazio ou null setar a data de hoje. Mesma coisa para data final