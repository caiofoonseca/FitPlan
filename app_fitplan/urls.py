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
    path('medidas/', views.medidas, name='medidas'),
    path('upload-medida/', views.upload_medida, name='upload_medida'),
    path('excluir-medida/<int:medida_id>/', views.excluir_medida, name='excluir_medida'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)