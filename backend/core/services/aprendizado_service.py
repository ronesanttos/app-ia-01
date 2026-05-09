from ..models import Previsao
from collections import Counter
from ..ml import obter_bonus_por_numero

def ajustar_por_historico(previsao):
    bonus = obter_bonus_por_numero()
    
    previsao = sorted(
        previsao,
        key=lambda x: bonus.get(x,0),
        reverse=True
    )
    
    return previsao[:10]

def extrair_padroes_erro(limite=100):
    previsoes = Previsao.objects.exclude(acuracia=None).order_by('-criada_em')[:limite]
    
    erros = []
    acertos = []
    
    for p in previsoes:
        previstos = set(p.numeros_previstos)
        reais = set(p.numeros_reais or [])
        
        erros.extend(previstos - reais)   # numeros errados
        acertos.extend(previstos & reais) # numeros certos
        
    return {
        "erros": Counter(erros),
        "acertos": Counter(acertos)
    }