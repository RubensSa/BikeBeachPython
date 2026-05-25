from django.db import models
from django.contrib.auth.models import User


class Bicicleta(models.Model):
    nome = models.CharField(max_length=120)
    modelo = models.CharField(max_length=120)
    cor = models.CharField(max_length=50, blank=True)
    valor_hora = models.DecimalField(max_digits=6, decimal_places=2)
    disponivel = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='bikes/', blank=True, null=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bicicletas')

    def __str__(self):
        return f"{self.nome} ({self.modelo})"


class Aluguel(models.Model):
    bicicleta = models.ForeignKey(Bicicleta, on_delete=models.CASCADE, related_name='alugueis')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alugueis')
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Aluguel {self.bicicleta} por {self.usuario}"
