from django.db import models

class Lista(models.Model):
    numeros = models.JSONField()
    criada_em = models.DateTimeField(auto_now_add=True)
    
class Resultado(models.Model):
    nao_repete = models.JSONField()
    repete = models.JSONField()
    falta = models.JSONField()
    
    criada_em = models.DateTimeField(auto_now_add=True)
    

class Previsao(models.Model):
    tipo = models.CharField(max_length=50) 

    numeros_previstos = models.JSONField()
    numeros_reais = models.JSONField(null=True, blank=True)
    
    probabilidades = models.JSONField(null=True, blank=True)


    acertos = models.IntegerField(null=True, blank=True)
    taxa_acerto = models.FloatField(null=True, blank=True)
    acuracia = models.FloatField(null=True, blank=True)
    
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.criada_em}"