from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your views here.

def index(request):
    #- indica que ele vai colocar em ordem decrescente
    lista_questoes=Question.objects.order_by('-pub_date')[:5]
    context={'lista_questoes':lista_questoes}
    return render(request,'index.html',context)
def details(request,question_id):
    response=f'Você está visualizando a questão {question_id}'
    return HttpResponse(response)
def results(request,question_id):
    response=f'Resultados da questão {question_id}'
    return HttpResponse(response)
def vote(request,question_id):
    response=f'Votação para a questão {question_id}'
    return HttpResponse(response)