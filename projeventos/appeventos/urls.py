from django.urls import path
#from .views import index,listar_eventos,listar_atividades,exibir_form_inscricao,registrar_inscricao,listar_participantes
from .views import EventoView,AtividadeView,AtividadeParticipanteView,InscricaoView,MinistranteListView,MinistranteCreateUpdateView,MinistranteDeleteView,ParticipanteCreateView,EventosLoginView,EventosLogoutView,AvalicaoCreateView,ToggleDarkModeView,FormContatoView
from django.views.generic import TemplateView
app_name='appeventos'
#urlpatterns=[
#    path('',index,name='index'),
#    path('eventos/listar',listar_eventos,name='listar_eventos'),
#    path('eventos/<int:evento_id>/atividades/listar',listar_atividades,name='listar_atividades'),
#    path('eventos/atividades/<int:atividade_id>/inscrever',exibir_form_inscricao,name='exibir_form_inscricao'),
#    path('eventos/atividades/<int:atividade_id>/registrar',registrar_inscricao,name="registrar_inscricao"),
#    path('eventos/atividades/<int:atividade_id>/participantes',listar_participantes,name='listar_participantes')
#]

urlpatterns=[
    path('',TemplateView.as_view(template_name='appeventos/index.html'),name='index'),
    path('eventos/listar',EventoView.as_view(),name='listar_eventos'),
    path('eventos/<int:evento_id>/atividades/listar',AtividadeView.as_view(),name='listar_atividades'),
    path('eventos/atividades/<int:atividade_id>/inscrever',InscricaoView.as_view(),name='exibir_form_inscricao'),
    path('eventos/atividades/<int:atividade_id>/registrar',InscricaoView.as_view(),name="registrar_inscricao"),
    path('eventos/atividades/<int:atividade_id>/participantes',AtividadeParticipanteView.as_view(),name='listar_participantes'),
    path('eventos/atividades/<int:atividade_id>/registrar_presenca',AtividadeParticipanteView.as_view(),name='registrar_presenca'),
    path('eventos/atividades/<int:atividade_id>/avaliar',AvalicaoCreateView.as_view(),name='avaliar_atividade'),
    path('ministrantes',MinistranteListView.as_view(),name='listar_ministrantes'),
    path('ministrantes/cadastrar',MinistranteCreateUpdateView.as_view(),name='cadastrar_ministrante'),
    path('ministrante/<int:ministrante_id>/editar',MinistranteCreateUpdateView.as_view(),name='editar_ministrante'),
    path('ministrante/<int:pk>/excluir',MinistranteDeleteView.as_view(),name='excluir_ministrante'),
    path('participantes/registrar',ParticipanteCreateView.as_view(),name='registrar_participante'),
    path('darkmode/',ToggleDarkModeView.as_view(),name='darkmode'),
    path('contato/',FormContatoView.as_view(),name='contato'),
    path('login/',EventosLoginView.as_view(),name='login'),
    path('logout/',EventosLogoutView.as_view(),name='logout'),
    ]