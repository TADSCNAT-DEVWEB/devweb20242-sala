from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<h1> Bem-vindo à aplicação Enquete</h1>")
def exibir(request):
    return HttpResponse("<h1>Nova Rota de Exibição</h1>")