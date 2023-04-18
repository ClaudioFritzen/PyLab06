from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.messages import constants

from django.contrib import auth


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        #### Validações
        
        # validaçao dos campos nao podem estar vazio
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Exitem campos vazios')
            return redirect(reverse('cadastro'))
        
        user = User.objects.filter(username=username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Usuario já existe')
            return redirect(reverse('cadastro'))  
         
        # validação para ver se existe esse email no banco ja
        email = User.objects.filter(email=email)
        if email.exists():
            messages.add_message(request, constants.WARNING, 'Email já utilizado')
            return render(request, 'cadastro.html', {'nome': username, 'senha': senha, 'confirmar_senha': confirmar_senha})
        ## Fazer a validação de força da senha 
        if len(senha) <= 8:
            messages.add_message(request, constants.WARNING, 'Senha precisa ser maior que 8 caractes')
            return render(request,'cadastro.html', {'nome': username, 'email': email})
        

        if not (senha == confirmar_senha): 
            messages.add_message(request, constants.ERROR, 'Senhas diferentes')   
            return redirect(reverse('cadastro'))
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso!')
        user.save()
        return redirect(reverse('login'))

        
        



def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect(reverse('login'))
        
        auth.login(request, user)
        return redirect('/eventos/novo_evento/')

def logout(request):
    return redirect(reverse('login'))