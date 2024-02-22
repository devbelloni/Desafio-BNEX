from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=100, null=False)
    descricao = models.TextField(null=False)
    valor = models.FloatField(null=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_modificacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
