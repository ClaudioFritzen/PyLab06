from django.shortcuts import render,redirect,get_object_or_404

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Evento,Certificado

from django.contrib import messages
from django.contrib.messages import constants

from django.http import Http404

## gerar csv
import csv
from secrets import token_urlsafe

import os
from django.conf import settings


### 
from PIL import Image, ImageDraw, ImageFont

from io import BytesIO

import sys
###
import datetime

@login_required


# Create your views here.
@login_required
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')

        nome = nome.strip()
        if len(nome) <=5:
            messages.add_message(request, constants.ERROR,
                                 'Nome deve ter mais que 5 caractes')
            return redirect('/eventos/novo_evento/')
            
        descricao = descricao.strip()
        if len(descricao) <=10:
            messages.add_message(request, constants.ERROR,
                                 'Nome deve ter mais que 5 caractes')
            return redirect('/eventos/novo_evento/')



        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')
        
        logo = request.FILES.get('logo')
        

        ## UTILIZANDO O CHAT GPT PARA MELHORAR O NOSSO CODIGO
         # tamanho da img que pode ser recebida
        if 'logo' in request.FILES:
            logo = request.FILES['logo']    
            if logo:
                if logo.size > 100_000_000:
                    messages.add_message(
                        request,
                        constants.ERROR,
                        'A logo da empresa deve ter menos de 10MB',
                    )
                    return redirect('/eventos/novo_evento/')
            else:
                # Se o logo estiver vazio, defina como None
                logo = None
        else:
            # Se a chave 'logo' não estiver em request.FILES, defina logo como None
            logo = None
        
        # Salvar o logo (mesmo que seja None)
        #nova_empresa.logo = logo
        #nova_empresa.save()

        #### Tratando o erro de quando salvamos vazio a data de inicio
        if not data_inicio:
            data_inicio = datetime.date.today()

        if not data_termino:
            data_termino = datetime.date.today()

        if len(carga_horaria) <=0:
            messages.add_message(request, constants.WARNING, 'Insira uma carga horaria!')
            
            return redirect('/eventos/novo_evento/')

        

        evento = Evento(
            criador=request.user,
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )
    
        evento.save()
        
        messages.add_message(request, constants.SUCCESS, 'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))


@login_required
def gerenciar_evento(request):
    if request.method == "GET":

        ## fazendo o filtro
        nome_filtro = request.GET.get('nome')
        eventos = Evento.objects.filter(criador=request.user)

        # TODO  fazer outros filtros
        if nome_filtro:
            eventos = eventos.filter(nome__contains=nome_filtro)
        
        return render(request, 'gerenciar_evento.html', {'eventos':eventos})


@login_required
def inscrever_evento(request, id):
		# Validar login
    evento = get_object_or_404(Evento, id=id)
    if request.method == "GET":
        return render(request, 'inscrever_evento.html', {'evento': evento})
    
    elif request.method == "POST":

        ### validar se o usuario já um participante
        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, constants.SUCCESS, 'Inscrição realizada com sucesso')
        return redirect(f'/eventos/inscrever_evento/{id}/')
    
def participantes_evento(request, id):
    evento = get_object_or_404(Evento, id=id)

    ## vendo se o evento é seu
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')
    

    if request.method == "GET":
        participantes = evento.participantes.all()[::3]
        return render(request, 'participantes_evento.html', {'evento': evento, 'participantes': participantes})
    
def gerar_csv(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')
    
    participantes = evento.participantes.all()
    
    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=",")
        for participante in participantes:
            x = (participante.username, participante.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')  

def certificados_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')
    if request.method == "GET":
        qtd_certificados = evento.participantes.all().count() - Certificado.objects.filter(evento=evento).count()
        return render(request, 'certificados_evento.html', {'evento': evento, 'qtd_certificados': qtd_certificados})


from io import BytesIO  
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont
import sys

def gerar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')

    path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
    path_fonte = os.path.join(settings.BASE_DIR, 'templates/static/fontes/arimo.ttf')
    for participante in evento.participantes.all():
        # TODO: Validar se já existe certificado desse participante para esse evento
        img = Image.open(path_template)
        path_template = os.path.join(settings.BASE_DIR, 'templates/static/evento/img/template_certificado.png')
        draw = ImageDraw.Draw(img)
        fonte_nome = ImageFont.truetype(path_fonte, 60)
        fonte_info = ImageFont.truetype(path_fonte, 30)
        draw.text((230, 651), f"{participante.username}", font=fonte_nome, fill=(0, 0, 0))
        draw.text((761, 782), f"{evento.nome}", font=fonte_info, fill=(0, 0, 0))
        draw.text((816, 849), f"{evento.carga_horaria} horas", font=fonte_info, fill=(0, 0, 0))
        output = BytesIO()
        img.save(output, format="PNG", quality=100)
        output.seek(0)
        img_final = InMemoryUploadedFile(output,
                                        'ImageField',
                                        f'{token_urlsafe(8)}.png',
                                        'image/jpeg',
                                        sys.getsizeof(output),
                                        None)
        certificado_gerado = Certificado(
            certificado=img_final,
            participante=participante,
            evento=evento,
        )
        certificado_gerado.save()
    
    messages.add_message(request, constants.SUCCESS, 'Certificados gerados')
    return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))


def procurar_certificado(request, id):
    evento = get_object_or_404(Evento, id=id)
    if not evento.criador == request.user:
        raise Http404('Esse evento não é seu')
    email = request.POST.get('email')
    certificado = Certificado.objects.filter(evento=evento).filter(participante__email=email).first()
    if not certificado:
        messages.add_message(request, constants.WARNING, 'Certificado não encontrado')
        return redirect(reverse('certificados_evento', kwargs={'id': evento.id}))
    
    return redirect(certificado.certificado.url)