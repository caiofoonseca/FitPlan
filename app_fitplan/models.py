from django.db import models
from django.contrib.auth.models import User

class Progresso(models.Model):
    imagem = models.ImageField(upload_to='progresso/')
    data = models.DateField()

    def __str__(self):
        return f"Progresso de {self.data}"

class Medida(models.Model):
    peso = models.FloatField()
    altura = models.FloatField()
    cintura = models.FloatField()
    quadril = models.FloatField()
    data = models.DateField()

    def __str__(self):
        return f"Medida de {self.data}"

class Treino(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    intensidade = models.CharField(max_length=50)
    duracao = models.CharField(max_length=50)
    local = models.CharField(max_length=50)
    data = models.DateField(auto_now_add=True)
    exercicios = models.JSONField() 

    def __str__(self):
        return f"Treino de {self.data} - {self.intensidade}, {self.duracao}, {self.local}"

class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    exercicio = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.usuario.username} - Favorito: {self.exercicio}"