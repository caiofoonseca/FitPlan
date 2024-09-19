from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),  # Certifique-se de que está usando 'login/' e não 'login'
    path('menu/', views.menu_view, name='menu'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
]
