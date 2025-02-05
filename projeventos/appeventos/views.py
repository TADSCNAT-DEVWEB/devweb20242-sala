from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.views.generic import ListView,DeleteView

from appeventos.models import Atividade,Evento,Inscricao,Participante,Ministrante

class EventoView(ListView):
    model=Evento
    paginate_by=2
    context_object_name="eventos"
    queryset=Evento.objects.order_by("-data")
    template_name="appeventos/eventos/lista.html"

class AtividadeView(View):
    template='appeventos/atividades/lista.html'
    def get(self,request,evento_id):
        evento=get_object_or_404(Evento,pk=evento_id)
        criterio=request.GET.get('criterio')
        if criterio==None:
            atividades=Atividade.objects.filter(evento=evento).order_by('-data','hora')
        else:
            atividades=Atividade.objects.filter(evento=evento,titulo__icontains=criterio).order_by('-data','hora')
        if atividades.count()==0:
            messages.error(request=request,message="Evento sem Atividades ou Nenhuma atividade encontrada com o critério informado")
            context={'nome_evento':evento.nome,'evento_id':evento.id,'criterio':criterio}
            return render(request,template_name=self.template,context=context)
        else:
            context={'atividades':atividades,'nome_evento':evento.nome,'criterio':criterio,'evento_id':evento.id}
            return render(request,template_name=self.template,context=context)

class AtividadeParticipanteView(View):
    def get(self,request,atividade_id):
        criterio=request.GET.get('criterio')
        context=self.buscaInscricoes(criterio,atividade_id)
        return render(request,template_name='appeventos/atividades/inscritos.html',context=context)
    def post(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        inscricoes_ids=request.POST.getlist("inscricoes_ids")
        for inscricao_id in inscricoes_ids:
            marcado=f'inscricao_{inscricao_id}' in request.POST
            Inscricao.objects.filter(id=inscricao_id).update(presenca=marcado)
        messages.success(request=request,message="Presenças Registradas com Sucesso!")
        context=self.buscaInscricoes(request.POST.get('criterio'),atividade_id)
        return render(request,template_name='appeventos/atividades/inscritos.html',context=context)
    
    def buscaInscricoes(self, criterio,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        if criterio==None:
            inscricoes=Inscricao.objects.filter(atividade=atividade).order_by("participante__nome")
        else:
            inscricoes=Inscricao.objects.filter(atividade=atividade,participante__nome__icontains=criterio).order_by("participante__nome")
        context={
            'atividade_id':atividade.id,
            'atividade_titulo':atividade.titulo,
            'inscricoes':inscricoes,
            'criterio':criterio
        }
        return context
class InscricaoView(View):
    def get(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        participantes=Participante.objects.order_by('nome')
        context={'atividade':atividade,'participantes':participantes}
        return render(request,template_name='appeventos/atividades/inscricoes.html',context=context)
    def post(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        participante=get_object_or_404(Participante,pk=request.POST['participante'])
        try:
            inscricao=Inscricao(atividade=atividade,participante=participante)
            inscricao.save()
            return redirect("appeventos:listar_atividades",evento_id=atividade.evento.id)
        except ValidationError as error:
            messages.error(request,message=error.message)
            return redirect('appeventos:exibir_form_inscricao',atividade_id=atividade.id)

class MinistranteListView(ListView):
    model=Ministrante
    context_object_name="ministrantes"
    template_name="appeventos/ministrantes/lista.html"
    paginate_by=3

    def get_queryset(self):
        queryset=Ministrante.objects.order_by("nome")
        criterio=self.request.GET.get("criterio")
        if criterio:
            queryset=queryset.filter(nome__icontains=criterio).order_by("nome")
        return queryset

class MinistranteCreateUpdateView(View):
    template_name="appeventos/ministrantes/form.html"
    def get(self,request,*args,**kwargs):
        ministrante_id=kwargs.get("ministrante_id")
        if ministrante_id:
            ministrante=get_object_or_404(Ministrante,pk=ministrante_id)
        else:
            ministrante=None
        context={"ministrante":ministrante}
        return render(request=request,template_name=self.template_name,context=context)
    
    def post(self,request,*args,**kwargs):
        ministrante_id=kwargs.get("ministrante_id")
        nome=request.POST.get('nome')
        data_nascimento=request.POST.get('data_nascimento')
        link_curriculo=request.POST.get('link_curriculo')
        if ministrante_id:
            ministrante=get_object_or_404(Ministrante,pk=ministrante_id)
            ministrante.nome=nome
            ministrante.data_nascimento=data_nascimento
            ministrante.link_curriculo=link_curriculo
        else:
            ministrante=Ministrante(nome=nome,data_nascimento=data_nascimento,link_curriculo=link_curriculo)
        try:
            ministrante.full_clean()
            ministrante.save()
            messages.success(request=request,message=f"Ministrante {ministrante.nome} Salvo com Sucesso")
            return redirect("appeventos:listar_ministrantes")
        except ValidationError as error:
            for atributo, error_list in error.message_dict.items():
                for error in error_list:
                    messages.error(request=request,message=f"{error}")
            context={'ministrante':ministrante}
            return render(request=request,template_name=self.template_name,context=context)

class MinistranteDeleteView(DeleteView):
    model=Ministrante
    template_name="appeventos/ministrantes/excluir.html"
    #https://docs.djangoproject.com/en/5.1/ref/urlresolvers/#reverse-lazy
    success_url=reverse_lazy("appeventos:listar_ministrantes")