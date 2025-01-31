from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Evento,Atividade,Participante,Inscricao

# Create your views here.

def index(request):
    return render(request,template_name='appeventos/index.html')

def listar_eventos(request):
    eventos=Evento.objects.order_by('-data')
    context={'eventos':eventos}
    return render(request,template_name='appeventos/eventos/lista.html',context=context)

def registrar_inscricao(request,atividade_id):
    if request.method=='POST':
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        participante=get_object_or_404(Participante,pk=int(request.POST['participante']))

        try:
            inscricao=Inscricao(atividade=atividade,participante=participante)
            inscricao.save()
            return redirect("appeventos:listar_atividades",evento_id=atividade.evento.id)
        except ValidationError as error:
            messages.error(request,message=str(error))
            return redirect("appeventos:exibir_form_inscricao",atividade_id=atividade.id)

def exibir_form_inscricao(request,atividade_id):
    atividade=get_object_or_404(Atividade,pk=atividade_id)
    participantes=Participante.objects.order_by('nome')
    context={'atividade':atividade,'participantes':participantes}
    return render(request,template_name='appeventos/atividades/inscricoes.html',context=context)
def listar_participantes(request,atividade_id):
    atividade=get_object_or_404(Atividade,pk=atividade_id)
    criterio=request.GET.get('criterio')
    if criterio==None:
        participantes=atividade.participantes.all()
    else:
        participantes=atividade.participantes.filter(nome__icontains=criterio)
    context={
        'atividade_id':atividade.id,
        'atividade_titulo':atividade.titulo,
        'participantes':participantes
    }
    return render(request,template_name='appeventos/atividades/lista_participantes.html',context=context)
def listar_atividades(request,evento_id):
    evento=get_object_or_404(Evento,pk=evento_id)
    criterio=request.GET.get('criterio')
    if criterio==None:
        atividades=Atividade.objects.filter(evento=evento).order_by('-data','hora')
    else:
        atividades=Atividade.objects.filter(evento=evento,titulo__icontains=criterio).order_by('-data','hora')
    if atividades.count()==0:
        messages.error(request=request,message="Evento sem Atividades ou Nenhuma atividade encontrada com o critério informado")
        context={'nome_evento':evento.nome,'evento_id':evento.id}
        return render(request,template_name='appeventos/atividades/lista.html',context=context)
    else:
        context={'atividades':atividades,'nome_evento':evento.nome,'evento_id':evento.id}
        return render(request,template_name='appeventos/atividades/lista.html',context=context)