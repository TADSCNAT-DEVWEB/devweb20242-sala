from django.db import models

from django.core.exceptions import ValidationError

# Create your models here.

class Ministrante(models.Model):
    nome = models.CharField(max_length=150,verbose_name="Nome")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    link_curriculo = models.URLField(verbose_name="Link do Currículo")

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=155,verbose_name="Nome")
    data = models.DateField(verbose_name="Data")
    local = models.CharField(max_length=200,verbose_name="Local")

    def __str__(self):
        return self.nome
    
class Participante(models.Model):
    nome = models.CharField(max_length=150,verbose_name="Nome")
    telefone =  models.CharField(max_length=20,verbose_name="Telefone")
    email = models.EmailField(max_length=100,verbose_name="Email")

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    TIPOS=(
        ('MI','Minicurso'),
        ('PR','Palestra'),
        ('OF','Oficina'),
    )
    data = models.DateField(verbose_name="Data da Atividade")
    hora = models.TimeField(verbose_name="Hora da Atividade")
    local = models.CharField(max_length=255,verbose_name="Local")
    titulo = models.CharField(max_length=255,verbose_name="Título")
    capacidade = models.IntegerField(verbose_name="Capacidade")
    tipo=models.CharField(max_length=2,verbose_name="Tipo de Atividade",choices=TIPOS,default='MI')
    ministrante = models.ForeignKey(Ministrante, on_delete=models.SET_NULL,verbose_name="Ministrante",related_name="atividades",null=True,blank=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="atividades",verbose_name="Evento")
    participantes=models.ManyToManyField(Participante,through='Inscricao',related_name="atividades")

    def tem_vaga(self):
        return self.participantes.count()<self.capacidade

    def __str__(self):
        return f'{self.evento}-{self.titulo}'

class Inscricao(models.Model):
    data = models.DateField(verbose_name="Data da Inscrição",auto_now_add=True)
    participante=models.ForeignKey(Participante,on_delete=models.CASCADE,verbose_name="Participante",related_name="inscricoes")
    atividade=models.ForeignKey(Atividade,on_delete=models.CASCADE,verbose_name="Atividade",related_name="inscricoes")
    presenca=models.BooleanField(verbose_name="Presença",default=False)

    def __str__(self):
        return f'{self.atividade.evento}-{self.atividade.titulo}-{self.participante}'

    def save(self,*args,**kwargs):
        if not self.atividade.tem_vaga():
            raise ValidationError("Não é possível realizar a inscrição por falta de vagas!")
        return super().save(*args,**kwargs)

    class Meta:
        verbose_name_plural="Inscrições"

class Certificado(models.Model):
    data_emissao=models.DateField(verbose_name="Data do Certificado",auto_now_add=True)
    inscricao=models.OneToOneField(Inscricao,verbose_name="Inscrição",
                                   on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.inscricao}'
    
    def save(self,*args,**kwargs):
        if not self.inscricao.presenca:
            raise ValidationError("Não é possível gerar certificado para participante ausente!")
        return super().save(*args,**kwargs)

class Avaliacao(models.Model):
    nota=models.IntegerField(verbose_name="Nota")
    comentario=models.TextField(verbose_name="Comentário")
    inscricao=models.OneToOneField(Inscricao,verbose_name="Inscrição",
                                   on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.inscricao}-{self.nota}'
    
    def save(self,*args,**kwargs):
        if not self.inscricao.presenca:
            raise ValidationError("Não é possível registrar avaliação para participante ausente!")
        return super().save(*args,**kwargs)   
    class Meta:
        verbose_name_plural="Avaliações"