from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Question

# Create your views here.

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
    response=f'Resultados da questão {question_id}'
    return HttpResponse(response)
def vote(request,question_id):
    response=f'Votação para a questão {question_id}'
    return HttpResponse(response)