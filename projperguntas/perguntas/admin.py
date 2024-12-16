from django.contrib import admin
from .models import Usuario,Pergunta,Tema,Resposta
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Pergunta)
admin.site.register(Tema)
admin.site.register(Resposta)
