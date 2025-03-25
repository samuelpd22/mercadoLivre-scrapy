from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=500)  
    imagem = models.URLField(blank=True, null=True, max_length=500)  
    preco_original = models.CharField(max_length=100, blank=True, null=True)  
    preco = models.CharField(max_length=100, blank=True, null=True)  
    parcelamento = models.CharField(max_length=100, blank=True, null=True)  
    desconto = models.CharField(max_length=50, blank=True, null=True)  
    link = models.URLField(blank=True, null=True, max_length=500)  
    tipo_entrega = models.CharField(max_length=50, blank=True, null=True)  
    frete_gratis = models.CharField(max_length=50, blank=True, null=True)  
 


    def __str__(self):
        return self.nome
