from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.files.storage import default_storage
from .models import Progresso, Medida, Treino, Favorito
from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse

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
        return redirect('agrupamento_muscular') 
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

def gerar_exercicios(intensidade, duracao, local, agrupamento):
    treino_opcoes = {

         ('Leve', '45MIN', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão de braço", "series": 3, "repeticoes": 12},
            {"nome": "Supino com halteres", "series": 3, "repeticoes": 10},
            {"nome": "Tríceps banco", "series": 3, "repeticoes": 15},
            {"nome": "Crucifixo", "series": 3, "repeticoes": 10},
            {"nome": "Tríceps unilateral", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão declinada", "series": 4, "repeticoes": 10},
            {"nome": "Supino inclinado com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps no banco", "series": 3, "repeticoes": 15},
            {"nome": "Crucifixo com halteres", "series": 3, "repeticoes": 10},
            {"nome": "Pullover", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão inclinada", "series": 4, "repeticoes": 15},
            {"nome": "Supino reto", "series": 4, "repeticoes": 10},
            {"nome": "Tríceps testa", "series": 4, "repeticoes": 12},
            {"nome": "Fly", "series": 4, "repeticoes": 12},
            {"nome": "Crucifixo inclinado", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '45MIN', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino na máquina", "series": 3, "repeticoes": 12},
            {"nome": "Crucifixo na máquina", "series": 3, "repeticoes": 12},
            {"nome": "Tríceps corda", "series": 3, "repeticoes": 15},
            {"nome": "Supino inclinado com barra", "series": 3, "repeticoes": 10},
            {"nome": "Tríceps pulley", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino reto", "series": 4, "repeticoes": 10},
            {"nome": "Crossover", "series": 3, "repeticoes": 15},
            {"nome": "Paralelas", "series": 3, "repeticoes": 10},
            {"nome": "Fly inclinado", "series": 4, "repeticoes": 10},
            {"nome": "Tríceps pulley com corda", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR 30MIN', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino declinado", "series": 4, "repeticoes": 12},
            {"nome": "Crossover na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps coice", "series": 4, "repeticoes": 12},
            {"nome": "Fly na máquina", "series": 3, "repeticoes": 12},
            {"nome": "Paralelas com peso", "series": 3, "repeticoes": 10},
        ],
        ('Leve', '45MIN', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão de braço", "series": 3, "repeticoes": 15},
            {"nome": "Tríceps banco", "series": 3, "repeticoes": 15},
            {"nome": "Flexão inclinada", "series": 3, "repeticoes": 12},
            {"nome": "Pullover com garrafa de água", "series": 3, "repeticoes": 10},
            {"nome": "Flexão diamante", "series": 3, "repeticoes": 10},
        ],
        ('Leve', '1HR', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão declinada", "series": 4, "repeticoes": 12},
            {"nome": "Flexão com clap", "series": 3, "repeticoes": 10},
            {"nome": "Tríceps no banco", "series": 3, "repeticoes": 15},
            {"nome": "Flexão fechada", "series": 3, "repeticoes": 10},
            {"nome": "Flexão spartan", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão inclinada", "series": 4, "repeticoes": 15},
            {"nome": "Tríceps banco com elevação de perna", "series": 3, "repeticoes": 12},
            {"nome": "Flexão declinada", "series": 4, "repeticoes": 12},
            {"nome": "Pullover com mochila", "series": 3, "repeticoes": 15},
            {"nome": "Flexão diamantada", "series": 3, "repeticoes": 15},
        ],

        ('Moderado', '45MIN', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão de braço", "series": 4, "repeticoes": 15},
            {"nome": "Supino com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps banco", "series": 4, "repeticoes": 15},
            {"nome": "Flexão inclinada", "series": 3, "repeticoes": 15},
            {"nome": "Pullover com peso", "series": 3, "repeticoes": 10},
        ],
        ('Moderado', '1HR', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão declinada", "series": 4, "repeticoes": 12},
            {"nome": "Supino inclinado com halteres", "series": 4, "repeticoes": 10},
            {"nome": "Tríceps no banco", "series": 4, "repeticoes": 15},
            {"nome": "Flexão com clap", "series": 4, "repeticoes": 8},
            {"nome": "Crucifixo com halteres", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '1HR 30MIN', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão diamante", "series": 4, "repeticoes": 12},
            {"nome": "Supino reto com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps francês", "series": 4, "repeticoes": 10},
            {"nome": "Flexão fechada", "series": 4, "repeticoes": 15},
            {"nome": "Crucifixo inclinado", "series": 3, "repeticoes": 10},
        ],
        ('Moderado', '45MIN', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino reto", "series": 3, "repeticoes": 12},
            {"nome": "Crossover", "series": 3, "repeticoes": 12},
            {"nome": "Tríceps corda", "series": 4, "repeticoes": 15},
            {"nome": "Supino inclinado com barra", "series": 3, "repeticoes": 10},
            {"nome": "Tríceps francês com barra", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '1HR', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino declinado", "series": 4, "repeticoes": 12},
            {"nome": "Crossover na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps coice", "series": 4, "repeticoes": 12},
            {"nome": "Fly na máquina", "series": 3, "repeticoes": 12},
            {"nome": "Paralelas com peso", "series": 3, "repeticoes": 10},
        ],
        ('Moderado', '1HR 30MIN', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino inclinado", "series": 4, "repeticoes": 10},
            {"nome": "Crossover na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps corda", "series": 4, "repeticoes": 12},
            {"nome": "Peck deck", "series": 3, "repeticoes": 15},
            {"nome": "Supino com barra", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '45MIN', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão de braço", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps banco", "series": 4, "repeticoes": 15},
            {"nome": "Flexão aberta", "series": 3, "repeticoes": 15},
            {"nome": "Pullover com garrafa", "series": 3, "repeticoes": 10},
            {"nome": "Flexão declinada", "series": 4, "repeticoes": 10},
        ],
        ('Moderado', '1HR', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão com clap", "series": 4, "repeticoes": 12},
            {"nome": "Flexão inclinada", "series": 4, "repeticoes": 10},
            {"nome": "Tríceps no banco", "series": 4, "repeticoes": 15},
            {"nome": "Pullover com peso", "series": 3, "repeticoes": 12},
            {"nome": "Flexão fechada", "series": 3, "repeticoes": 10},
        ],
        ('Moderado', '1HR 30MIN', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão diamante", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps banco", "series": 4, "repeticoes": 15},
            {"nome": "Flexão fechada", "series": 3, "repeticoes": 15},
            {"nome": "Pullover com mochila", "series": 3, "repeticoes": 10},
            {"nome": "Flexão inclinada", "series": 3, "repeticoes": 15},
        ],

        ('Intenso', '45MIN', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão explosiva", "series": 5, "repeticoes": 10},
            {"nome": "Supino com halteres", "series": 5, "repeticoes": 8},
            {"nome": "Tríceps banco", "series": 5, "repeticoes": 12},
            {"nome": "Flexão declinada", "series": 4, "repeticoes": 12},
            {"nome": "Flexão com clap", "series": 4, "repeticoes": 10},
        ],
        ('Intenso', '1HR', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Supino inclinado com halteres", "series": 5, "repeticoes": 10},
            {"nome": "Flexão diamante", "series": 5, "repeticoes": 12},
            {"nome": "Tríceps no banco", "series": 4, "repeticoes": 15},
            {"nome": "Crucifixo com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Flexão espartana", "series": 3, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Em casa', 'Peito e tríceps'): [
            {"nome": "Flexão fechada", "series": 5, "repeticoes": 12},
            {"nome": "Supino reto com halteres", "series": 5, "repeticoes": 10},
            {"nome": "Flexão com clap", "series": 4, "repeticoes": 15},
            {"nome": "Tríceps francês", "series": 4, "repeticoes": 10},
            {"nome": "Pullover", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '45MIN', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino reto com barra", "series": 4, "repeticoes": 8},
            {"nome": "Crossover", "series": 5, "repeticoes": 15},
            {"nome": "Tríceps corda", "series": 4, "repeticoes": 12},
            {"nome": "Supino inclinado", "series": 4, "repeticoes": 10},
            {"nome": "Tríceps francês", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '1HR', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino declinado", "series": 4, "repeticoes": 8},
            {"nome": "Crossover", "series": 4, "repeticoes": 10},
            {"nome": "Tríceps testa", "series": 5, "repeticoes": 12},
            {"nome": "Crucifixo inclinado", "series": 4, "repeticoes": 10},
            {"nome": "Paralelas", "series": 3, "repeticoes": 12},
        ],
        ('Intenso', '1HR 30MIN', 'Na academia', 'Peito e tríceps'): [
            {"nome": "Supino com barra", "series": 5, "repeticoes": 10},
            {"nome": "Fly na máquina", "series": 5, "repeticoes": 12},
            {"nome": "Tríceps coice", "series": 4, "repeticoes": 10},
            {"nome": "Crossover", "series": 4, "repeticoes": 10},
            {"nome": "Flexão diamante", "series": 3, "repeticoes": 15},
        ],
        ('Intenso', '45MIN', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão de braço", "series": 5, "repeticoes": 15},
            {"nome": "Flexão espartana", "series": 5, "repeticoes": 12},
            {"nome": "Tríceps banco", "series": 5, "repeticoes": 12},
            {"nome": "Flexão explosiva", "series": 4, "repeticoes": 10},
            {"nome": "Flexão inclinada", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '1HR', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão declinada", "series": 5, "repeticoes": 12},
            {"nome": "Flexão com clap", "series": 4, "repeticoes": 10},
            {"nome": "Flexão diamante", "series": 4, "repeticoes": 15},
            {"nome": "Tríceps no banco", "series": 5, "repeticoes": 12},
            {"nome": "Pullover com peso", "series": 3, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Ao ar livre', 'Peito e tríceps'): [
            {"nome": "Flexão explosiva", "series": 5, "repeticoes": 15},
            {"nome": "Flexão espartana", "series": 4, "repeticoes": 12},
            {"nome": "Tríceps banco", "series": 5, "repeticoes": 15},
            {"nome": "Pullover com mochila", "series": 4, "repeticoes": 12},
            {"nome": "Flexão diamante", "series": 3, "repeticoes": 15},
        ],
         ('Leve', '45MIN', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Remada unilateral com halteres", "series": 3, "repeticoes": 12},
            {"nome": "Rosca direta com halteres", "series": 3, "repeticoes": 15},
            {"nome": "Rosca concentrada", "series": 3, "repeticoes": 12},
            {"nome": "Remada baixa", "series": 3, "repeticoes": 10},
            {"nome": "Encolhimento com halteres", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Pulldown com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca martelo", "series": 4, "repeticoes": 10},
            {"nome": "Remada curvada com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Flexão australiana", "series": 3, "repeticoes": 10},
            {"nome": "Rosca invertida", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR 30MIN', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Remada baixa com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Rosca direta com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Pullover com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Encolhimento com halteres", "series": 3, "repeticoes": 20},
            {"nome": "Remada curvada", "series": 4, "repeticoes": 12},
        ],
        ('Leve', '45MIN', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Pulldown", "series": 3, "repeticoes": 12},
            {"nome": "Remada sentada", "series": 3, "repeticoes": 12},
            {"nome": "Rosca direta na máquina", "series": 3, "repeticoes": 15},
            {"nome": "Pullover", "series": 3, "repeticoes": 10},
            {"nome": "Rosca concentrada", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Pulldown na máquina", "series": 4, "repeticoes": 10},
            {"nome": "Remada baixa", "series": 4, "repeticoes": 12},
            {"nome": "Rosca alternada", "series": 4, "repeticoes": 15},
            {"nome": "Pullover na máquina", "series": 3, "repeticoes": 12},
            {"nome": "Rosca martelo", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Remada curvada com barra", "series": 4, "repeticoes": 12},
            {"nome": "Pulldown com barra", "series": 4, "repeticoes": 15},
            {"nome": "Rosca direta", "series": 4, "repeticoes": 12},
            {"nome": "Pullover com cabo", "series": 3, "repeticoes": 12},
            {"nome": "Encolhimento na máquina", "series": 4, "repeticoes": 12},
        ],
        ('Leve', '45MIN', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Flexão australiana", "series": 3, "repeticoes": 12},
            {"nome": "Remada com elástico", "series": 3, "repeticoes": 15},
            {"nome": "Rosca direta com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Encolhimento com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Remada baixa com elástico", "series": 3, "repeticoes": 10},
        ],
        ('Leve', '1HR', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Remada curvada com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca concentrada com elástico", "series": 4, "repeticoes": 10},
            {"nome": "Pullover com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca martelo com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Flexão australiana", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR 30MIN', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Flexão australiana com peso", "series": 4, "repeticoes": 12},
            {"nome": "Remada com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca direta com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Pullover com elástico", "series": 3, "repeticoes": 10},
            {"nome": "Remada curvada", "series": 3, "repeticoes": 12},
        ],

        ('Moderado', '45MIN', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Remada curvada com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Rosca direta com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Rosca concentrada", "series": 4, "repeticoes": 12},
            {"nome": "Pullover com halteres", "series": 3, "repeticoes": 12},
            {"nome": "Remada baixa com halteres", "series": 3, "repeticoes": 10},
        ],
        ('Moderado', '1HR', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Pullover com elástico", "series": 4, "repeticoes": 10},
            {"nome": "Remada curvada com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Rosca martelo", "series": 4, "repeticoes": 15},
            {"nome": "Flexão australiana", "series": 3, "repeticoes": 15},
            {"nome": "Rosca direta com halteres", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '1HR 30MIN', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Remada com halteres", "series": 5, "repeticoes": 12},
            {"nome": "Pullover com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Rosca direta com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Encolhimento com halteres", "series": 3, "repeticoes": 15},
            {"nome": "Rosca concentrada", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '45MIN', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Remada sentada na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Pulldown", "series": 3, "repeticoes": 12},
            {"nome": "Rosca direta na barra", "series": 4, "repeticoes": 12},
            {"nome": "Pullover na máquina", "series": 3, "repeticoes": 15},
            {"nome": "Remada baixa", "series": 4, "repeticoes": 10},
        ],
        ('Moderado', '1HR', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Remada curvada com barra", "series": 4, "repeticoes": 15},
            {"nome": "Pullover", "series": 4, "repeticoes": 12},
            {"nome": "Rosca martelo", "series": 4, "repeticoes": 10},
            {"nome": "Encolhimento", "series": 4, "repeticoes": 15},
            {"nome": "Rosca concentrada", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '1HR 30MIN', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Remada curvada", "series": 5, "repeticoes": 10},
            {"nome": "Pullover com barra", "series": 4, "repeticoes": 12},
            {"nome": "Rosca direta", "series": 4, "repeticoes": 15},
            {"nome": "Pulldown", "series": 3, "repeticoes": 12},
            {"nome": "Remada baixa com halteres", "series": 4, "repeticoes": 10},
        ],
        ('Moderado', '45MIN', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Flexão australiana", "series": 4, "repeticoes": 12},
            {"nome": "Remada com elástico", "series": 3, "repeticoes": 15},
            {"nome": "Rosca direta com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Encolhimento com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Remada baixa com elástico", "series": 3, "repeticoes": 10},
        ],
        ('Moderado', '1HR', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Remada curvada com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca concentrada com elástico", "series": 4, "repeticoes": 10},
            {"nome": "Pullover com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca martelo com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Flexão australiana", "series": 3, "repeticoes": 15},
        ],
        ('Moderado', '1HR 30MIN', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Flexão australiana com peso", "series": 4, "repeticoes": 12},
            {"nome": "Remada com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca direta com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Pullover com elástico", "series": 3, "repeticoes": 10},
            {"nome": "Remada curvada", "series": 3, "repeticoes": 12},
        ],

        ('Intenso', '45MIN', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Remada com elástico", "series": 5, "repeticoes": 15},
            {"nome": "Pullover", "series": 4, "repeticoes": 12},
            {"nome": "Rosca direta com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Rosca concentrada", "series": 4, "repeticoes": 15},
            {"nome": "Remada curvada", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '1HR', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Pullover com barra", "series": 5, "repeticoes": 12},
            {"nome": "Rosca direta com barra", "series": 5, "repeticoes": 15},
            {"nome": "Rosca martelo", "series": 4, "repeticoes": 10},
            {"nome": "Remada curvada", "series": 4, "repeticoes": 12},
            {"nome": "Flexão australiana com peso", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Em casa', 'Costas e bíceps'): [
            {"nome": "Remada curvada com barra", "series": 5, "repeticoes": 15},
            {"nome": "Pullover com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Rosca direta com halteres", "series": 4, "repeticoes": 10},
            {"nome": "Remada curvada com barra", "series": 5, "repeticoes": 12},
            {"nome": "Encolhimento com halteres", "series": 4, "repeticoes": 10},
        ],
        ('Intenso', '45MIN', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Remada sentada", "series": 5, "repeticoes": 12},
            {"nome": "Pulldown", "series": 4, "repeticoes": 15},
            {"nome": "Rosca direta com barra", "series": 4, "repeticoes": 10},
            {"nome": "Pullover na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Remada curvada com barra", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '1HR', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Pulldown com pegada aberta", "series": 5, "repeticoes": 12},
            {"nome": "Remada baixa", "series": 4, "repeticoes": 15},
            {"nome": "Rosca concentrada com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Pullover com cabo", "series": 3, "repeticoes": 12},
            {"nome": "Encolhimento na máquina", "series": 4, "repeticoes": 10},
        ],
        ('Intenso', '1HR 30MIN', 'Na academia', 'Costas e bíceps'): [
            {"nome": "Remada curvada com barra", "series": 5, "repeticoes": 12},
            {"nome": "Pulldown com pegada neutra", "series": 5, "repeticoes": 15},
            {"nome": "Rosca direta com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Pullover com barra", "series": 4, "repeticoes": 10},
            {"nome": "Rosca martelo com halteres", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '45MIN', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Flexão australiana com peso", "series": 5, "repeticoes": 15},
            {"nome": "Remada com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Rosca direta com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Encolhimento com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Remada baixa com elástico", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '1HR', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Remada curvada com elástico", "series": 5, "repeticoes": 12},
            {"nome": "Rosca concentrada com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Pullover com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca martelo com elástico", "series": 4, "repeticoes": 10},
            {"nome": "Flexão australiana com peso", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '1HR 30MIN', 'Ao ar livre', 'Costas e bíceps'): [
            {"nome": "Flexão australiana com sobrecarga", "series": 5, "repeticoes": 15},
            {"nome": "Remada com elástico forte", "series": 5, "repeticoes": 12},
            {"nome": "Rosca direta com elástico resistente", "series": 4, "repeticoes": 12},
            {"nome": "Pullover com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Remada curvada com halteres", "series": 4, "repeticoes": 15},
        ],
        ('Leve', '45MIN', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento com peso corporal", "series": 3, "repeticoes": 15},
            {"nome": "Stiff com halteres", "series": 3, "repeticoes": 12},
            {"nome": "Afundo sem peso", "series": 3, "repeticoes": 12},
            {"nome": "Ponte de glúteo", "series": 3, "repeticoes": 15},
            {"nome": "Extensão de quadril", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento búlgaro", "series": 4, "repeticoes": 12},
            {"nome": "Stiff unilateral", "series": 4, "repeticoes": 12},
            {"nome": "Afundo reverso", "series": 3, "repeticoes": 15},
            {"nome": "Elevação de quadril", "series": 4, "repeticoes": 15},
            {"nome": "Passada com halteres", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento sumô", "series": 4, "repeticoes": 12},
            {"nome": "Stiff com barra improvisada", "series": 3, "repeticoes": 12},
            {"nome": "Ponte com uma perna", "series": 4, "repeticoes": 10},
            {"nome": "Afundo búlgaro", "series": 3, "repeticoes": 12},
            {"nome": "Extensão de quadril com peso", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '45MIN', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Leg press", "series": 4, "repeticoes": 12},
            {"nome": "Extensão de perna", "series": 3, "repeticoes": 15},
            {"nome": "Cadeira flexora", "series": 3, "repeticoes": 12},
            {"nome": "Afundo com halteres", "series": 4, "repeticoes": 10},
            {"nome": "Ponte com barra", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento smith", "series": 4, "repeticoes": 12},
            {"nome": "Cadeira extensora", "series": 4, "repeticoes": 15},
            {"nome": "Stiff com barra", "series": 3, "repeticoes": 12},
            {"nome": "Ponte com peso", "series": 4, "repeticoes": 15},
            {"nome": "Afundo smith", "series": 3, "repeticoes": 15},
        ],
        ('Leve', '1HR 30MIN', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento livre", "series": 4, "repeticoes": 12},
            {"nome": "Extensão de quadril", "series": 4, "repeticoes": 12},
            {"nome": "Cadeira flexora", "series": 3, "repeticoes": 15},
            {"nome": "Passada na esteira", "series": 3, "repeticoes": 12},
            {"nome": "Ponte com peso", "series": 4, "repeticoes": 10},
        ],
        ('Leve', '45MIN', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Caminhada em subida", "series": 1, "repeticoes": 30},
            {"nome": "Agachamento com peso corporal", "series": 3, "repeticoes": 15},
            {"nome": "Ponte de glúteo", "series": 3, "repeticoes": 20},
            {"nome": "Elevação de perna em banco", "series": 3, "repeticoes": 15},
            {"nome": "Afundo com peso corporal", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida leve", "series": 1, "repeticoes": 45},
            {"nome": "Agachamento búlgaro", "series": 3, "repeticoes": 12},
            {"nome": "Elevação de quadril", "series": 3, "repeticoes": 15},
            {"nome": "Afundo com salto", "series": 3, "repeticoes": 10},
            {"nome": "Passada com peso corporal", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida moderada", "series": 1, "repeticoes": 60},
            {"nome": "Agachamento sumô", "series": 4, "repeticoes": 12},
            {"nome": "Afundo com peso corporal", "series": 4, "repeticoes": 12},
            {"nome": "Elevação de quadril", "series": 4, "repeticoes": 15},
            {"nome": "Ponte para posterior de coxa", "series": 4, "repeticoes": 12},
        ],

        ('Moderado', '45MIN', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Stiff unilateral", "series": 3, "repeticoes": 15},
            {"nome": "Agachamento búlgaro", "series": 3, "repeticoes": 15},
            {"nome": "Passada lateral", "series": 3, "repeticoes": 12},
            {"nome": "Extensão de quadril", "series": 3, "repeticoes": 15},
            {"nome": "Afundo reverso", "series": 3, "repeticoes": 15},
        ],
        ('Moderado', '1HR', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento sumô com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Stiff com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Elevação de quadril com peso", "series": 4, "repeticoes": 10},
            {"nome": "Passada frontal", "series": 3, "repeticoes": 15},
            {"nome": "Afundo lateral", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '1HR 30MIN', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Levantamento terra", "series": 4, "repeticoes": 12},
            {"nome": "Agachamento búlgaro com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Ponte com uma perna", "series": 4, "repeticoes": 12},
            {"nome": "Elevação de quadril com peso", "series": 4, "repeticoes": 15},
            {"nome": "Extensão de quadril unilateral", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '45MIN', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento livre", "series": 4, "repeticoes": 12},
            {"nome": "Cadeira extensora", "series": 3, "repeticoes": 15},
            {"nome": "Leg press", "series": 4, "repeticoes": 15},
            {"nome": "Flexora deitado", "series": 4, "repeticoes": 10},
            {"nome": "Afundo smith", "series": 3, "repeticoes": 15},
        ],
        ('Moderado', '1HR', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Cadeira abdutora", "series": 4, "repeticoes": 15},
            {"nome": "Extensora de perna", "series": 3, "repeticoes": 15},
            {"nome": "Stiff com barra", "series": 4, "repeticoes": 12},
            {"nome": "Agachamento guiado", "series": 4, "repeticoes": 12},
            {"nome": "Afundo na barra smith", "series": 4, "repeticoes": 15},
        ],
        ('Moderado', '1HR 30MIN', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento sumô", "series": 4, "repeticoes": 12},
            {"nome": "Stiff com barra", "series": 4, "repeticoes": 12},
            {"nome": "Cadeira flexora", "series": 3, "repeticoes": 15},
            {"nome": "Leg press horizontal", "series": 3, "repeticoes": 15},
            {"nome": "Ponte com barra", "series": 4, "repeticoes": 10},
        ],
        ('Moderado', '45MIN', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida em subida", "series": 1, "repeticoes": 30},
            {"nome": "Ponte de glúteo", "series": 3, "repeticoes": 20},
            {"nome": "Agachamento com peso corporal", "series": 3, "repeticoes": 15},
            {"nome": "Afundo com salto", "series": 3, "repeticoes": 15},
            {"nome": "Passada na grama", "series": 3, "repeticoes": 15},
        ],
        ('Moderado', '1HR', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida leve", "series": 1, "repeticoes": 45},
            {"nome": "Agachamento sumô", "series": 3, "repeticoes": 15},
            {"nome": "Afundo com peso corporal", "series": 3, "repeticoes": 12},
            {"nome": "Ponte de glúteo", "series": 4, "repeticoes": 15},
            {"nome": "Ponte unilateral", "series": 4, "repeticoes": 10},
        ],
        ('Moderado', '1HR 30MIN', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida intervalada", "series": 1, "repeticoes": 60},
            {"nome": "Agachamento com salto", "series": 3, "repeticoes": 15},
            {"nome": "Passada com peso corporal", "series": 3, "repeticoes": 12},
            {"nome": "Ponte para glúteo", "series": 3, "repeticoes": 15},
            {"nome": "Elevação de quadril", "series": 3, "repeticoes": 10},
        ],

        ('Intenso', '45MIN', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento com salto", "series": 4, "repeticoes": 15},
            {"nome": "Stiff com halteres pesados", "series": 4, "repeticoes": 12},
            {"nome": "Afundo com salto", "series": 4, "repeticoes": 10},
            {"nome": "Ponte com peso", "series": 4, "repeticoes": 15},
            {"nome": "Passada explosiva", "series": 3, "repeticoes": 12},
        ],
        ('Intenso', '1HR', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento búlgaro", "series": 4, "repeticoes": 15},
            {"nome": "Ponte com peso", "series": 4, "repeticoes": 12},
            {"nome": "Stiff com barra improvisada", "series": 4, "repeticoes": 15},
            {"nome": "Ponte com perna elevada", "series": 4, "repeticoes": 10},
            {"nome": "Passada rápida", "series": 3, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Em casa', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento sumô com peso", "series": 4, "repeticoes": 12},
            {"nome": "Afundo búlgaro com peso", "series": 4, "repeticoes": 15},
            {"nome": "Ponte com perna elevada", "series": 4, "repeticoes": 12},
            {"nome": "Elevação de quadril", "series": 4, "repeticoes": 15},
            {"nome": "Stiff com barra", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '45MIN', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento com barra", "series": 4, "repeticoes": 10},
            {"nome": "Leg press pesado", "series": 4, "repeticoes": 12},
            {"nome": "Cadeira extensora", "series": 4, "repeticoes": 15},
            {"nome": "Stiff com barra", "series": 4, "repeticoes": 10},
            {"nome": "Afundo smith", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '1HR', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Hack machine", "series": 4, "repeticoes": 10},
            {"nome": "Agachamento livre com peso", "series": 4, "repeticoes": 12},
            {"nome": "Cadeira flexora pesada", "series": 4, "repeticoes": 12},
            {"nome": "Leg press inclinado", "series": 4, "repeticoes": 10},
            {"nome": "Extensão de quadril no cabo", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Na academia', 'Posterior de perna e quadríceps'): [
            {"nome": "Agachamento profundo com barra", "series": 5, "repeticoes": 10},
            {"nome": "Leg press pesado", "series": 5, "repeticoes": 12},
            {"nome": "Cadeira extensora com carga máxima", "series": 4, "repeticoes": 12},
            {"nome": "Stiff com barra", "series": 4, "repeticoes": 12},
            {"nome": "Afundo guiado", "series": 4, "repeticoes": 12},
        ],
        ('Intenso', '45MIN', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Sprint em subida", "series": 1, "repeticoes": 20},
            {"nome": "Agachamento com salto", "series": 4, "repeticoes": 15},
            {"nome": "Ponte de glúteo com perna elevada", "series": 4, "repeticoes": 12},
            {"nome": "Afundo reverso com peso corporal", "series": 4, "repeticoes": 15},
            {"nome": "Step-up em caixa", "series": 4, "repeticoes": 10},
        ],
        ('Intenso', '1HR', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida com inclinação", "series": 1, "repeticoes": 30},
            {"nome": "Agachamento unilateral", "series": 4, "repeticoes": 12},
            {"nome": "Ponte de glúteo", "series": 4, "repeticoes": 15},
            {"nome": "Afundo búlgaro", "series": 4, "repeticoes": 10},
            {"nome": "Pliometria para pernas", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Ao ar livre', 'Posterior de perna e quadríceps'): [
            {"nome": "Corrida intensa", "series": 1, "repeticoes": 40},
            {"nome": "Agachamento com salto", "series": 5, "repeticoes": 15},
            {"nome": "Afundo alternado", "series": 5, "repeticoes": 12},
            {"nome": "Ponte com perna elevada", "series": 5, "repeticoes": 10},
            {"nome": "Step-up em banco", "series": 4, "repeticoes": 12},
        ],
        ('Leve', '45MIN', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Elevação lateral com garrafas", "series": 3, "repeticoes": 15},
            {"nome": "Elevação frontal com garrafas", "series": 3, "repeticoes": 15},
            {"nome": "Rotação externa com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Rosca punho", "series": 3, "repeticoes": 15},
            {"nome": "Flexão de ombro contra parede", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento de ombro", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com garrafas", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal", "series": 3, "repeticoes": 15},
            {"nome": "Rosca inversa com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Alongamento de ombro", "series": 2, "repeticoes": 30},
        ],
        ('Leve', '1HR 30MIN', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com garrafas", "series": 4, "repeticoes": 15},
            {"nome": "Rotação interna com elástico", "series": 3, "repeticoes": 12},
            {"nome": "Flexão de punho com garrafas", "series": 4, "repeticoes": 15},
        ],

        ('Leve', '45MIN', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Elevação lateral na máquina", "series": 3, "repeticoes": 12},
            {"nome": "Elevação frontal com halteres", "series": 3, "repeticoes": 15},
            {"nome": "Rosca punho", "series": 3, "repeticoes": 15},
            {"nome": "Desenvolvimento máquina", "series": 3, "repeticoes": 12},
            {"nome": "Alongamento de ombro", "series": 2, "repeticoes": 30},
        ],
        ('Leve', '1HR', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres", "series": 3, "repeticoes": 12},
            {"nome": "Elevação lateral", "series": 3, "repeticoes": 15},
            {"nome": "Rosca punho", "series": 3, "repeticoes": 15},
            {"nome": "Elevação frontal com halteres", "series": 3, "repeticoes": 15},
            {"nome": "Remada alta", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com barra", "series": 4, "repeticoes": 12},
            {"nome": "Rotação interna com halteres", "series": 3, "repeticoes": 12},
            {"nome": "Rosca inversa", "series": 4, "repeticoes": 12},
        ],

        ('Leve', '45MIN', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexões inclinadas", "series": 3, "repeticoes": 12},
            {"nome": "Elevação lateral", "series": 3, "repeticoes": 15},
            {"nome": "Flexão com rotação", "series": 3, "repeticoes": 12},
            {"nome": "Alongamento de ombro", "series": 2, "repeticoes": 30},
            {"nome": "Rotação externa com elástico", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Elevação frontal com elástico", "series": 3, "repeticoes": 15},
            {"nome": "Rosca punho com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Elevação lateral com elástico", "series": 3, "repeticoes": 15},
            {"nome": "Flexão inclinada com rotação", "series": 3, "repeticoes": 12},
        ],
        ('Leve', '1HR 30MIN', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Elevação lateral", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal", "series": 4, "repeticoes": 15},
            {"nome": "Rotação interna", "series": 4, "repeticoes": 12},
            {"nome": "Desenvolvimento de ombro com elástico", "series": 4, "repeticoes": 12},
            {"nome": "Rosca punho com garrafa", "series": 4, "repeticoes": 15},
        ],
        ('Moderado', '45MIN', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com halteres", "series": 3, "repeticoes": 15},
            {"nome": "Rosca punho", "series": 3, "repeticoes": 20},
            {"nome": "Flexão de ombro", "series": 3, "repeticoes": 12},
        ],
        ('Moderado', '1HR', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal", "series": 4, "repeticoes": 12},
            {"nome": "Rosca inversa", "series": 3, "repeticoes": 20},
            {"nome": "Prancha com elevação de ombro", "series": 3, "repeticoes": 30},
        ],
        ('Moderado', '1HR 30MIN', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento de ombro", "series": 5, "repeticoes": 10},
            {"nome": "Elevação lateral", "series": 5, "repeticoes": 12},
            {"nome": "Elevação frontal", "series": 4, "repeticoes": 12},
            {"nome": "Prancha com elevação de ombro", "series": 4, "repeticoes": 45},
            {"nome": "Rosca inversa", "series": 4, "repeticoes": 15},
        ],

        ('Moderado', '45MIN', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com barra", "series": 4, "repeticoes": 10},
            {"nome": "Elevação lateral na máquina", "series": 4, "repeticoes": 12},
            {"nome": "Elevação frontal com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Remada alta com barra", "series": 3, "repeticoes": 15},
            {"nome": "Rosca punho", "series": 3, "repeticoes": 20},
        ],
        ('Moderado', '1HR', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres", "series": 4, "repeticoes": 10},
            {"nome": "Elevação lateral", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Remada alta", "series": 3, "repeticoes": 12},
            {"nome": "Flexão de punho na barra", "series": 3, "repeticoes": 20},
        ],
        ('Moderado', '1HR 30MIN', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres", "series": 5, "repeticoes": 10},
            {"nome": "Elevação lateral", "series": 5, "repeticoes": 15},
            {"nome": "Elevação frontal", "series": 5, "repeticoes": 12},
            {"nome": "Remada baixa", "series": 4, "repeticoes": 15},
            {"nome": "Rosca punho", "series": 4, "repeticoes": 15},
        ],

        ('Moderado', '45MIN', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexão inclinada", "series": 4, "repeticoes": 15},
            {"nome": "Elevação lateral com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Rosca punho com elástico", "series": 3, "repeticoes": 20},
            {"nome": "Prancha com rotação de ombro", "series": 3, "repeticoes": 30},
        ],
        ('Moderado', '1HR', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexão com elevação de braço", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com elástico", "series": 4, "repeticoes": 15},
            {"nome": "Rosca punho com elástico", "series": 3, "repeticoes": 20},
            {"nome": "Remada com elástico", "series": 4, "repeticoes": 12},
        ],
        ('Moderado', '1HR 30MIN', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexão de ombro", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com elástico", "series": 5, "repeticoes": 15},
            {"nome": "Elevação frontal com elástico", "series": 5, "repeticoes": 15},
            {"nome": "Rosca punho", "series": 4, "repeticoes": 20},
            {"nome": "Alongamento de ombro", "series": 3, "repeticoes": 30},
        ],
        ('Intenso', '45MIN', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento militar", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com halteres pesados", "series": 4, "repeticoes": 15},
            {"nome": "Flexão de ombro com peso", "series": 3, "repeticoes": 20},
            {"nome": "Rosca punho com halteres", "series": 4, "repeticoes": 15},
            {"nome": "Prancha com toque de ombro", "series": 4, "repeticoes": 30},
        ],
        ('Intenso', '1HR', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres", "series": 5, "repeticoes": 12},
            {"nome": "Elevação lateral em 45 graus", "series": 4, "repeticoes": 15},
            {"nome": "Remada alta com halteres", "series": 4, "repeticoes": 12},
            {"nome": "Rosca inversa", "series": 4, "repeticoes": 15},
            {"nome": "Flexão de punho com halteres", "series": 4, "repeticoes": 20},
        ],
        ('Intenso', '1HR 30MIN', 'Em casa', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento militar", "series": 5, "repeticoes": 12},
            {"nome": "Elevação lateral unilateral", "series": 5, "repeticoes": 12},
            {"nome": "Elevação frontal alternada", "series": 5, "repeticoes": 12},
            {"nome": "Rosca punho", "series": 4, "repeticoes": 20},
            {"nome": "Prancha com rotação de ombro", "series": 4, "repeticoes": 30},
        ],

        ('Intenso', '45MIN', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com barra", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral na máquina", "series": 4, "repeticoes": 15},
            {"nome": "Elevação frontal com barra", "series": 4, "repeticoes": 12},
            {"nome": "Remada alta com barra", "series": 4, "repeticoes": 15},
            {"nome": "Rosca punho na máquina", "series": 3, "repeticoes": 20},
        ],
        ('Intenso', '1HR', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com halteres sentado", "series": 5, "repeticoes": 10},
            {"nome": "Elevação lateral", "series": 5, "repeticoes": 12},
            {"nome": "Elevação frontal com barra", "series": 4, "repeticoes": 15},
            {"nome": "Remada baixa", "series": 4, "repeticoes": 12},
            {"nome": "Rosca punho na máquina", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Na academia', 'Ombro e antebraço'): [
            {"nome": "Desenvolvimento com barra", "series": 5, "repeticoes": 12},
            {"nome": "Elevação lateral com pesos livres", "series": 5, "repeticoes": 15},
            {"nome": "Elevação frontal com barra", "series": 5, "repeticoes": 15},
            {"nome": "Remada alta", "series": 4, "repeticoes": 12},
            {"nome": "Rosca punho", "series": 4, "repeticoes": 20},
        ],

        ('Intenso', '45MIN', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexão inclinada", "series": 4, "repeticoes": 15},
            {"nome": "Elevação lateral com elástico", "series": 4, "repeticoes": 20},
            {"nome": "Elevação frontal com elástico", "series": 4, "repeticoes": 20},
            {"nome": "Rosca punho com elástico", "series": 3, "repeticoes": 25},
            {"nome": "Prancha com elevação de ombro", "series": 3, "repeticoes": 30},
        ],
        ('Intenso', '1HR', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexão de ombro com peso", "series": 4, "repeticoes": 12},
            {"nome": "Elevação lateral com elástico", "series": 4, "repeticoes": 20},
            {"nome": "Elevação frontal com elástico", "series": 4, "repeticoes": 20},
            {"nome": "Rosca punho", "series": 3, "repeticoes": 20},
            {"nome": "Remada com elástico", "series": 4, "repeticoes": 15},
        ],
        ('Intenso', '1HR 30MIN', 'Ao ar livre', 'Ombro e antebraço'): [
            {"nome": "Flexão de ombro", "series": 5, "repeticoes": 15},
            {"nome": "Elevação lateral com elástico", "series": 5, "repeticoes": 20},
            {"nome": "Elevação frontal com elástico", "series": 5, "repeticoes": 20},
            {"nome": "Rosca punho", "series": 4, "repeticoes": 20},
            {"nome": "Prancha com toque de ombro", "series": 4, "repeticoes": 30},
        ],
}
    return treino_opcoes.get((intensidade, duracao, local, agrupamento), [{"nome": "Exercício padrão", "series": 1, "repeticoes": 10}])

def gerar_treino_view(request, treino_id=None):
    if treino_id:
        treino = get_object_or_404(Treino, id=treino_id)
        exercicios = treino.exercicios
    else:
        intensidade = request.session.get('intensidade')
        duracao = request.session.get('duracao')
        local = request.session.get('local')
        agrupamento = request.session.get('agrupamento')

        if intensidade and duracao and local and agrupamento:
            exercicios = gerar_exercicios(intensidade, duracao, local, agrupamento)
            treino = Treino.objects.create(
                usuario=request.user,
                intensidade=intensidade,
                duracao=duracao,
                local=local,
                exercicios=exercicios
            )
        else:
            return redirect('menu')

    return render(request, 'treino.html', {'treino': treino, 'exercicios': exercicios})

def favoritar_exercicio(request, treino_id, exercicio):
    treino = get_object_or_404(Treino, id=treino_id)
    Favorito.objects.get_or_create(usuario=request.user, treino=treino, exercicio=exercicio)
    return redirect('treino', treino_id=treino_id)

def historico_treinos(request):
    treinos = Treino.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'historico_treinos.html', {'treinos': treinos})

def treinos_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user)
    return render(request, 'favoritos.html', {'favoritos': favoritos})

def agrupamento_muscular_view(request):
    if request.method == 'POST':
        agrupamento = request.POST.get('agrupamento')
        request.session['agrupamento'] = agrupamento
        return redirect('gerar_treino')
    return render(request, 'agrupamento_muscular.html')

def remover_favorito(request, favorito_id):
    favorito = get_object_or_404(Favorito, id=favorito_id, usuario=request.user)
    favorito.delete()
    return redirect('favoritos')