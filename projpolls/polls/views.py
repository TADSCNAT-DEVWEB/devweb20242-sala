from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question,Choice

# Create your views here.
'''
def index(request):
    #- indica que ele vai colocar em ordem decrescente
    lista_questoes=Question.objects.all()
    context={'lista':lista_questoes}
    return render(request,'index.html',context)
def details(request,question_id):
    questao=get_object_or_404(Question,pk=question_id)
    context={'questao':questao}
    return render(request,'details.html',context)
def results(request,question_id):
    questao=get_object_or_404(Question,pk=question_id)
    context={'questao':questao}
    return render(request,'results.html',context)
'''

def vote(request,question_id):
    questao=get_object_or_404(Question,pk=question_id)
    try:
        alternativa=questao.choice_set.get(pk=request.POST['alternativa'])
    except(KeyError,Choice.DoesNotExist):
        context={'questao':questao,'mensagem_erro':'Você não selecionou uma alternativa'}
        return render(request,'details.html',context)
    else:
        alternativa.votes+=1
        alternativa.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question_id,)))

def cadastrar_alternativa(request,question_id):
    questao=get_object_or_404(Question,pk=question_id)
    texto_alternativa=request.POST['alternativa']
    if len(texto_alternativa)==0:
        context={'questao':questao,'mensagem_erro':'Você não preencheu a alternativa'}
        return render(request,'form_alternativa.html',context)
    else:
        alternativa=Choice(question=questao,
                           choice_text=texto_alternativa)
        alternativa.save()
        return HttpResponseRedirect(reverse('polls:index'))

class IndexView(generic.ListView):
    context_object_name="lista"
    model=Question
    template_name='index.html'

class AlternativaView(generic.DetailView):
    model=Question
    context_object_name='questao'
    template_name='form_alternativa.html'

class DetailView(generic.DetailView):
    model=Question
    context_object_name='questao'
    template_name='details.html'

class ResultsView(generic.DetailView):
    model=Question
    context_object_name='questao'
    template_name='results.html'