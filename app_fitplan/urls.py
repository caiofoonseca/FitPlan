from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('intensidade/', views.intensidade_view, name='intensidade'),
    path('duracao/', views.duracao_view, name='duracao'),
    path('local/', views.local_view, name='local'),
    path('agrupamento_muscular/', views.agrupamento_muscular_view, name='agrupamento_muscular'),
    path('gerar_treino/', views.gerar_treino_view, name='gerar_treino'),
    path('calculadora-imc/', views.calculadora_imc, name='calculadoraimc'),
    path('progresso/', views.progresso, name='progresso'),
    path('upload-progresso/', views.upload_progresso, name='upload_progresso'),
    path('excluir-progresso/<int:progresso_id>/', views.excluir_progresso, name='excluir_progresso'),
    path('medidas/', views.medidas, name='medidas'),
    path('upload-medida/', views.upload_medida, name='upload_medida'),
    path('excluir-medida/<int:medida_id>/', views.excluir_medida, name='excluir_medida'),
    path('dicas-alimentares/', views.dicas_alimentares, name='dicas_alimentares'),
    path('historico_treinos/', views.historico_treinos, name='historico_treinos'),
    path('favoritos/', views.treinos_favoritos, name='treinos_favoritos'),
    path('favoritar_exercicio/<int:treino_id>/<str:exercicio>/', views.favoritar_exercicio, name='favoritar_exercicio'),
    path('remover_favorito/<int:favorito_id>/', views.remover_favorito, name='remover_favorito'),
    path('treino/<int:treino_id>/', views.gerar_treino_view, name='treino'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)