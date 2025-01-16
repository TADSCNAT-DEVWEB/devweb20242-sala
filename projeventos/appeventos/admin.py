from django.contrib import admin
from .models import Participante,Ministrante,Evento,Atividade,Inscricao,Avaliacao,Certificado

# Register your models here.

admin.site.register(Participante)
admin.site.register(Ministrante)
admin.site.register(Evento)
admin.site.register(Atividade)
admin.site.register(Inscricao)
admin.site.register(Avaliacao)
admin.site.register(Certificado)
