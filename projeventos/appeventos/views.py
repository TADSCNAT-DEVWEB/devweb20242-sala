from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.views.generic import ListView,DeleteView
from django.core.paginator import Paginator
import os
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from appeventos.models import Atividade,Evento,Inscricao,Participante,Ministrante,Avaliacao

def eh_participante(user):
    return hasattr(user,'participante')

def eh_administrador(user):
    return user.is_superuser

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
            paginator=Paginator(atividades,2)
            page_number=request.GET.get("page")
            page_obj=paginator.get_page(page_number)
            context={'atividades':atividades,'nome_evento':evento.nome,'criterio':criterio,'evento_id':evento.id,'page_obj':page_obj,'is_paginated':True}
            return render(request,template_name=self.template,context=context)

@method_decorator(user_passes_test(eh_administrador),name='dispatch')
class AtividadeParticipanteView(LoginRequiredMixin,View):
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

@method_decorator(user_passes_test(eh_participante),name='dispatch')
class InscricaoView(LoginRequiredMixin,View):
    template_name='appeventos/atividades/inscricoes.html'
    def get(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        context={'atividade':atividade}
        return render(request,template_name=self.template_name,context=context)
    def post(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        participante=request.user.participante
        try:
            inscricao=Inscricao(atividade=atividade,participante=participante)
            inscricao.save()
            messages.success(request,message='Inscrição realizada com sucesso')
            return redirect("appeventos:listar_atividades",evento_id=atividade.evento.id)
        except ValidationError as error:
            messages.error(request,message=error.message)
            return redirect('appeventos:listar_atividades',evento_id=atividade.evento.id)

@method_decorator(user_passes_test(eh_administrador),name='dispatch')
class MinistranteListView(ListView,LoginRequiredMixin):
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

@method_decorator(user_passes_test(eh_administrador),name='dispatch')
class MinistranteCreateUpdateView(View,LoginRequiredMixin):
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

@method_decorator(user_passes_test(eh_administrador),name='dispatch')
class MinistranteDeleteView(DeleteView,LoginRequiredMixin):
    model=Ministrante
    template_name="appeventos/ministrantes/excluir.html"
    success_url=reverse_lazy("appeventos:listar_ministrantes")
class MinistranteDeleteView(DeleteView):
    model=Ministrante
    template_name="appeventos/ministrantes/excluir.html"
    #https://docs.djangoproject.com/en/5.1/ref/urlresolvers/#reverse-lazy
    success_url=reverse_lazy("appeventos:listar_ministrantes")

class EventosLoginView(LoginView):
    template_name = 'appeventos/login.html'
    
    def form_invalid(self, form):
        # Exibe mensagem de erro para credenciais inválidas
        messages.error(self.request, "Credenciais inválidas. Por favor, verifique seu usuário e senha.")
        return super().form_invalid(form)


class EventosLogoutView(LogoutView):
    http_method_names=['get','post']

    def get(self, request, *args, **kwargs):
        # Adiciona a mensagem de sucesso para o logout via GET
        logout(request)
        messages.success(request, "Você foi desconectado com sucesso.")
        return redirect('appeventos:index')

    def post(self, request, *args, **kwargs):
        # Caso você queira tratar o POST também
        logout(request)
        messages.success(request, "Você foi desconectado com sucesso.")
        return redirect('appeventos:index')

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']

class ParticipanteCreateView(View):
    template_name="appeventos/participantes/form.html"
    def get(self,request):
        if request.user.is_authenticated:
            print(request.user)
            return redirect("appeventos:index")
        else:
            return render(request=request,template_name=self.template_name)
    def post(self,request):
        login=request.POST.get("login")
        nome=request.POST.get("nome")
        senha=request.POST.get("senha")
        email=request.POST.get("email")
        telefone=request.POST.get("telefone")
        foto=request.FILES.get('foto')
        if User.objects.filter(username=login).exists():
            messages.error(request,"Login já existente. Por favor, escolha outro")
            return render(request,self.template_name)
        if foto:
            ext = os.path.splitext(foto.name)[1].lower()  # Obtém a extensão, ex: '.jpg'
            if ext not in ALLOWED_EXTENSIONS:
                messages.error(request, "Tipo de arquivo inválido. Envie apenas imagens PNG ou JPG.")
                return render(request, self.template_name)
        
        #Cria o usuário Django

        user=User.objects.create_user(username=login,password=senha,email=email)
        user.save()

        participante=Participante(user=user,nome=nome,telefone=telefone,foto=foto)

        participante.save()

        messages.success(request=request,message="Participante cadastrado com sucesso")

        return redirect("appeventos:index")

@method_decorator(user_passes_test(eh_participante),name='dispatch')
class AvalicaoCreateView(LoginRequiredMixin,View):
    template_name='appeventos/avaliacoes/form.html'
    def get(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        try:
            inscricao=Inscricao.objects.get(atividade=atividade,participante=request.user.participante)
            print(request.user.participante.nome)
        except ObjectDoesNotExist as error:
            messages.error(request=request,message="Participante sem inscrição na atividade")
            return redirect('appeventos:listar_atividades',evento_id=atividade.evento.id)
        if inscricao.presenca:
            context={'atividade':atividade}
            return render(request,template_name=self.template_name,context=context)
        else:
            messages.error(request=request,message='Participante não esteve presente na atividade')
            return redirect('appeventos:listar_atividades',evento_id=atividade.evento.id)
    def post(self,request,atividade_id):
        atividade=get_object_or_404(Atividade,pk=atividade_id)
        inscricao=Inscricao.objects.get(atividade=atividade,participante=request.user.participante)
        nota=request.POST.get('nota')
        comentario=request.POST.get('comentario')
        try:
            avaliacao=Avaliacao(inscricao=inscricao,nota=nota,comentario=comentario)
            avaliacao.save()
            messages.success(request,message='Avaliação realizada com sucesso')
            return redirect("appeventos:listar_atividades",evento_id=atividade.evento.id)
        except ValidationError as error:
            messages.error(request,message=error.message)
            return redirect('appeventos:listar_atividades',evento_id=atividade.evento.id)