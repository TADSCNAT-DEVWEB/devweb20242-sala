from django import forms

class ContatoForm(forms.Form):
    assunto=forms.CharField()
    mensagem=forms.CharField()
    remetente=forms.EmailField()