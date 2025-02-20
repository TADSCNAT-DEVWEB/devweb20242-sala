from django import forms
from appeventos.models import Ministrante
class ContatoForm(forms.Form):
    assunto=forms.CharField()
    mensagem=forms.CharField(widget=forms.Textarea(attrs={'class':'textarea'}))
    remetente=forms.EmailField()

class MinistranteForm(forms.ModelForm):
    class Meta:
        model=Ministrante
        fields=['nome','data_nascimento','link_curriculo']