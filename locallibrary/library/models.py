from django.db import models

# Create your models here.

class Genre(models.Model):
    name=models.CharField(verbose_name="Nome",max_length=100)
    def __str__(self):
        return self.name

class Language(models.Model):
    name=models.CharField(verbose_name="Nome",max_length=200)
    def __str__(self):
        return self.name
    
class Author(models.Model):

    GENDER=(('F','Female'),('M','Male'))

    name=models.CharField(verbose_name="Nome",max_length=200)
    dateOfBirth=models.DateField(verbose_name="Data de Nascimento")
    dateOfDeath=models.DateField(verbose_name="Data de Falecimento",null=True,blank=True)
    gender=models.CharField(max_length=1,choices=GENDER,blank=True,verbose_name="Gênero",
                            help_text='Selecione o gênero da lista apresentada')

    def __str__(self):
        return self.name

class Book(models.Model):

    title=models.CharField(max_length=200)
    summary=models.TextField(max_length=100,help_text="Informe o sumário do Livro",verbose_name="Sumário")
    language=models.ForeignKey(Language,on_delete=models.SET_NULL,null=True,related_name="books")
    isbn=models.CharField(verbose_name='ISBN',max_length=13,unique=True,help_text='Informe o <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN</a>')
    authors=models.ManyToManyField(Author,related_name="books",help_text="Selecione os Autores do Livro",through='Authorship')
    genres=models.ManyToManyField(Genre,related_name="books",help_text="Selecione os Gêneros do Livro")

    def __str__(self):
        return self.title

class Authorship(models.Model):
    author=models.ForeignKey(Author,on_delete=models.CASCADE,verbose_name="Autor")
    book=models.ForeignKey(Book,on_delete=models.CASCADE,verbose_name="Livro")
    role=models.CharField(max_length=100,verbose_name="Papel")

    def __str__(self):
        return f'{self.book.title}-{self.role}'