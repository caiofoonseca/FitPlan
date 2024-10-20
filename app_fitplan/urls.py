from django.urls import path
from . import views

urlpatterns = [
     path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'), 
    path('menu/', views.menu_view, name='menu'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('intensidade/', views.intensidade_view, name='intensidade'),
    path('duracao/', views.duracao_view, name='duracao'),
    path('local/', views.local_view, name='local'),
    path('calculadora-imc/', views.calculadora_imc, name='calculadoraimc'),
    path('progresso/', views.progresso, name='progresso'), 
    path('upload-progresso/', views.upload_progresso, name='upload_progresso'),  
    path('excluir-progresso/<int:progresso_id>/', views.excluir_progresso, name='excluir_progresso'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)