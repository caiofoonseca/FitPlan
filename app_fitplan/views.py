from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Progresso, Medida  
from django.http import HttpResponse
from django.core.files.storage import default_storage

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

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, email=email, password=password, first_name=nome_completo)
            user.save()
            messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
            return redirect('login')  
        else:
            messages.error(request, 'O nome de usuário já existe. Tente outro.')
    
    return render(request, 'teladecadastro.html')

def menu_view(request):
    return render(request, 'telademenu.html')

def intensidade_view(request):
    if request.method == 'POST':
        intensidade = request.POST.get('intensidade')
        request.session['intensidade'] = intensidade
        return redirect('duracao')
    return render(request, 'teladeintensidade.html')

def duracao_view(request):
    if request.method == 'POST':
        duracao = request.POST.get('duracao')
        request.session['duracao'] = duracao
        return redirect('local')
    return render(request, 'teladeduracao.html')

def local_view(request):
    if request.method == 'POST':
        local = request.POST.get('local')
        request.session['local'] = local
        return redirect('menu') 
    return render(request, 'teladelocal.html')

def calculadora_imc(request):
    imc = None
    if request.method == 'POST':
        try:
            peso = float(request.POST.get('peso'))
            altura = float(request.POST.get('altura'))
            if altura > 0:
                imc = peso / (altura ** 2)
                imc = round(imc, 2) 
        except (ValueError, TypeError):
            imc = None

    return render(request, 'calculadoraimc.html', {'imc': imc})

def progresso(request):
    progressos = Progresso.objects.all()
    return render(request, 'progresso.html', {'progressos': progressos})

def upload_progresso(request):
    if request.method == 'POST':
        try:
            if 'imagem' not in request.FILES:
                return HttpResponse("Nenhum arquivo de imagem enviado", status=400)

            imagem = request.FILES['imagem']
            data = request.POST['data']

            file_name = default_storage.save(f'progresso/{imagem.name}', imagem)
            
            progresso = Progresso(imagem=file_name, data=data)
            progresso.save()

            return redirect('progresso')
        except Exception as e:
            return HttpResponse(f"Erro ao salvar o progresso: {str(e)}", status=500)
    return HttpResponse(status=400)

def excluir_progresso(request, progresso_id):
    progresso = get_object_or_404(Progresso, id=progresso_id)
    progresso.delete()
    return redirect('progresso')

def medidas(request):
    medidas = Medida.objects.all()  
    return render(request, 'medidas.html', {'medidas': medidas})

def upload_medida(request):
    if request.method == 'POST':
        try:
            peso = float(request.POST['peso'])
            altura = float(request.POST['altura'])
            cintura = float(request.POST['cintura'])
            quadril = float(request.POST['quadril'])
            data = request.POST['data']

            medida = Medida(peso=peso, altura=altura, cintura=cintura, quadril=quadril, data=data)
            medida.save()

            return redirect('medidas')
        except ValueError:
            return HttpResponse("Erro ao processar os dados da medida", status=400)
    return HttpResponse(status=400)

def excluir_medida(request, medida_id):
    medida = get_object_or_404(Medida, id=medida_id)
    medida.delete()
    return redirect('medidas')

def dicas_alimentares(request):
    return render(request, 'dicasalimentares.html')