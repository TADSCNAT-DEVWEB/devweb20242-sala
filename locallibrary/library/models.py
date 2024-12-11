from django.db import models

# Create your models here.

class Genre(models.Model):
    name=models.CharField(verbose_name="Nome",max_length=100)
    def __str__(self):
        return self.name
