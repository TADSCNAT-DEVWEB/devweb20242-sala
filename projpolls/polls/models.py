from django.db import models

class Question(models.Model):
    question_text=models.CharField(max_length=200,verbose_name="Texto da Questão")
    pub_date=models.DateTimeField(verbose_name="Data da Publicação")
class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200,verbose_name="Alternativa")
    votes=models.IntegerField(default=0)
