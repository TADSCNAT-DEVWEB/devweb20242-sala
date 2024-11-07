from django.db import models
import datetime
from django.utils import timezone
class Question(models.Model):
    question_text=models.CharField(max_length=200,verbose_name="Texto da Questão")
    pub_date=models.DateTimeField(verbose_name="Data da Publicação")
    def __str__(self):
        return self.question_text
    def foi_publicado_recentemente(self):
        return self.pub_date>=timezone.now()-datetime.timedelta(days=1)

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200,verbose_name="Alternativa")
    votes=models.IntegerField(default=0)
