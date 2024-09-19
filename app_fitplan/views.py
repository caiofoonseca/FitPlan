from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['email'] 
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')  
        else:
            return render(request, 'teladelogin.html', {'error': 'Email ou senha inválidos.'})
    else:
        return render(request, 'teladelogin.html')

def cadastro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        nome_completo = request.POST['nome_completo']
        email = request.POST['email']
        password = request.POST['password']

        # Verifica se o nome de usuário já existe
        if not User.objects.filter(username=username).exists():
            # Cria o usuário
            user = User.objects.create_user(username=username, email=email, password=password, first_name=nome_completo)
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
            return redirect('login')  # Redireciona para a tela de login após cadastro
        else:
            messages.error(request, 'O nome de usuário já existe. Tente outro.')
    
    return render(request, 'teladecadastro.html')

def menu_view(request):
    return render(request, 'telademenu.html')
