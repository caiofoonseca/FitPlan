from django.db import models

class Progresso(models.Model):
    imagem = models.ImageField(upload_to='progresso/')
    data = models.DateField()

    def __str__(self):
        return f"Progresso de {self.data}"