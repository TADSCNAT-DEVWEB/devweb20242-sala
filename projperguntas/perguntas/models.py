from django.db import models

# Create your models here.
class Usuario(models.Model):
    apelido=models.CharField(max_length=100,verbose_name="Apelido")
    ultima_postagem=models.DateTimeField(verbose_name="Data da Última Postagem",blank=True,null=True)
    def __str__(self):
        return self.apelido

class Tema(models.Model):
    titulo=models.CharField(max_length=100,verbose_name="Título")
    descricao=models.CharField(max_length=255,verbose_name="Descrição")
    arquivado=models.BooleanField(verbose_name="Arquivado",default=False)
    data=models.DateField(verbose_name="Data do Cadastro",auto_now_add=True)
    cadastrador=models.ForeignKey(Usuario,verbose_name="Cadastrador Por",on_delete=models.SET_NULL,related_name="temas",null=True)

    def __str__(self):
        return self.titulo

class Pergunta(models.Model):
    enunciado=models.CharField(max_length=200,verbose_name="Enunciado da Pergunta")
    data=models.DateField(verbose_name="Data de Cadastro",auto_now_add=True)
    curtidas=models.IntegerField(verbose_name="Número de Curtidas",default=0)
    cadastrador=models.ForeignKey(Usuario,verbose_name="Cadastrado Por",on_delete=models.SET_NULL,related_name="perguntas",null=True)

    def __str__(self):
        return self.enunciado

class Resposta(models.Model):
    texto=models.CharField(max_length=255,verbose_name="Resposta")
    data=models.DateTimeField(verbose_name="Data de Cadastro da Resposta",auto_now_add=True)
    curtidas=models.IntegerField(verbose_name="Curtidas",default=0)
    pergunta=models.ForeignKey(Pergunta,verbose_name="Pergunta",on_delete=models.CASCADE,related_name="respostas")
    cadastrador=models.ForeignKey(Usuario,verbose_name="Cadastrado Por",on_delete=models.SET_NULL,related_name="respostas",null=True)

    def __str__(self):
        return f'{self.cadastrador}-{self.pergunta}-{self.texto}'

