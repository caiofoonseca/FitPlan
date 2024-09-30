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
]