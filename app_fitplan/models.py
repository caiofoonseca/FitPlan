from django.db import models

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
