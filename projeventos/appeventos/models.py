# Create your models here.
from django.db import models
from django.db.models import Q,Count
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError




class Ministrante(models.Model):
    nome = models.CharField(max_length=150,verbose_name="Nome")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    link_curriculo = models.URLField(verbose_name="Link do Currículo")

    def __str__(self):
        return self.nome
    """
        Como estratégia de gerenciamento de erros, criamos um dicionário para reter as mensagens de erro por campo,
        de forma que o usuário receba as informações da forma correta e de uma única vez.
    """
    def clean(self):
        erros={} #Erros são gerados de uma única vez e gerada uma única vez.

        if len(self.nome.strip())<5:
            erros["nome"]="Nome não pode ter menos do que 5 caracteres"
        
        if self.data_nascimento > timezone.now().date():
            erros["data_nascimento"]="Data de Nascimento não pode ser no futuro"
        
        url_validator=URLValidator()

        try:
            url_validator(self.link_curriculo)
        except ValidationError:
            erros["link_curriculo"]="O Link do currículo precisa ser uma URL"

        if erros: #Gerado a exeção que inclui todos os erros
            raise ValidationError(erros)

class Evento(models.Model):
    nome = models.CharField(max_length=155,verbose_name="Nome")
    data = models.DateField(verbose_name="Data")
    local = models.CharField(max_length=200,verbose_name="Local")
    def __str__(self):
        return self.nome
    
    def get_total_inscritos(self):
        return Evento.objects.filter(id=self.id).aggregate(Count('atividades__participantes'))['atividades__participantes__count']
    
class Participante(models.Model):
    nome = models.CharField(max_length=150,verbose_name="Nome")
    telefone =  models.CharField(max_length=20,verbose_name="Telefone")
    email = models.EmailField(max_length=100,verbose_name="Email")

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    TIPOS=(('OF','Oficina'),
           ('PR','Palestra'),
           ('MI','Minicurso'))
    data = models.DateField(verbose_name="Data da Atividade")
    hora = models.TimeField(verbose_name="Hora da Atividade")
    local = models.CharField(max_length=255,verbose_name="Local")
    titulo = models.CharField(max_length=255,verbose_name="Título")
    capacidade = models.IntegerField(verbose_name="Capacidade")
    ministrante = models.ForeignKey(Ministrante, on_delete=models.SET_NULL,verbose_name="Ministrante",related_name="atividades",null=True)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="atividades",verbose_name="Evento")
    participantes=models.ManyToManyField(Participante,through='Inscricao',related_name="atividades")
    tipo=models.CharField(max_length=20,choices=TIPOS,verbose_name="Tipos",default='OF')

    def get_capacidade_restante(self):
        return self.capacidade-self.participantes.count()
    
    def tem_vaga(self):
        return self.get_capacidade_restante()>0

    def __str__(self):
        return f'{self.evento}-{self.titulo}'

class Inscricao(models.Model):
    data = models.DateField(verbose_name="Data da Inscrição",auto_now_add=True)
    participante=models.ForeignKey(Participante,on_delete=models.CASCADE,verbose_name="Participante",related_name="inscricoes")
    atividade=models.ForeignKey(Atividade,on_delete=models.CASCADE,verbose_name="Atividade",related_name="inscricoes")
    presenca=models.BooleanField(verbose_name="Presença",default=False)

    def __str__(self):
        return f'{self.atividade}-{self.participante}'
    
    def save(self, *args, **kwargs):
        if self._state.adding:  # Verifica se é uma nova inscrição
            if not self.atividade.tem_vaga():
                raise ValidationError("Atividade com vagas esgotadas")
            if self.atividade.participantes.filter(id=self.participante.id).count() != 0:
                raise ValidationError("Participante já inscrito nessa atividade")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural="Inscrições"

class Certificado(models.Model):
    data_emissao=models.DateField(verbose_name="Data do Certificado",auto_now_add=True)
    inscricao=models.OneToOneField(Inscricao,verbose_name="Inscrição",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.inscricao}-{self.data_emissao}'
    def save(self, *args,**kwargs):
        if not self.inscricao.presenca:
            raise ValidationError("Não é possível gerar certificado para participante ausente")
        return super().save(*args,**kwargs)

class Avaliacao(models.Model):
    nota=models.IntegerField(verbose_name="Nota")
    comentario=models.TextField(verbose_name="Comentário")
    #Igual ao Foreign Key, on_delete é obrigatório
    inscricao=models.OneToOneField(Inscricao,verbose_name="Inscrição",on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.inscricao}'
    
    def save(self, *args, **kwargs): #nessa validação é feia apenas durante o save
        if not self.inscricao.presenca:
            raise ValidationError("Não é possível realizar avaliação para participante ausente")
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural="Avaliações"