from django.db import models

# Create your models here.

class Ministrante(models.Model):
    nome = models.CharField(max_length=150,verbose_name="Nome")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    link_curriculo = models.URLField(verbose_name="Link do Currículo")

class Evento(models.Model):
    nome = models.CharField(max_length=155,verbose_name="Nome")
    data = models.DateField(verbose_name="Data")
    local = models.CharField(max_length=200,verbose_name="Local")
    

class Atividade(models.Model):
    data = models.DateField(verbose_name="Data da Atividade")
    hora = models.TimeField(verbose_name="Hora da Atividade")
    local = models.CharField(max_length=255,verbose_name="Local")
    titulo = models.CharField(max_length=255,verbose_name="Título")
    capacidade = models.IntegerField(verbose_name="Capacidade")
    ministrante = models.ForeignKey(Ministrante, on_delete=models.SET_NULL,verbose_name="Ministrante",related_name="atividades")
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="atividades",verbose_name="Evento")

class Participante(models.Model):
    nome = models.CharField(max_length=150,verbose_name="Nome")
    telefone =  models.CharField(max_length=20,verbose_name="Telefone")
    email = models.EmailField(max_length=100,verbose_name="Email")

class Inscricao(models.Model):
    data = models.DateField

