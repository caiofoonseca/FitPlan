from django.db import models

class Medida(models.Model):
    imagem = models.ImageField(upload_to='medidas/')
    data = models.DateField()

    def __str__(self):
        return f"Medida de {self.data}"