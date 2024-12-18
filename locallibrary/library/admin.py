from django.contrib import admin
from .models import Language,Genre,Author,Book,Authorship,BookInstance

# Register your models here.

admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Authorship)
admin.site.register(BookInstance)
