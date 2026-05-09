from django.contrib import admin
from core import models

@admin.register(models.Lista)
class ListaAdmin(admin.ModelAdmin):
    list_display = ('id','criada_em',)
    
@admin.register(models.Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    list_display = ('id','criada_em',)
    
@admin.register(models.Previsao)
class PrevisaoAdmin(admin.ModelAdmin):
    list_display = ('id','criada_em',)