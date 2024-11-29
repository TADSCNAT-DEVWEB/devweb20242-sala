from django.urls import path
from . import views
app_name='polls' #Código adicionado
urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('<int:pk>/',views.DetailView.as_view(),name='details'),
    path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),
    path('<int:pk>/alternativa/',views.AlternativaView.as_view(),name='alternativas'),
    path('<int:question_id>/alternativa/cadastrar',views.cadastrar_alternativa,name='cadastrar_alternativa'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
]