from ..models import Previsao
from ..utils import calcular_peso_previsao

def obter_bonus_por_numero():
    bonus = {i: 0 for i in range(100)}
    
    previsoes = Previsao.objects.exclude(acuracia=None).order_by('-id')[:100]
    
    for p in previsoes:
        peso = calcular_peso_previsao(p)
        
        for n in p.numeros_previstos:
            if n in p.numeros_reais:
                bonus[n] += 0.2 * peso
            else:
                bonus[n] -= 0.1 * peso
                
    max_val = max(abs(v) for v in bonus.values()) or 1
    
    for k in bonus:
        bonus[k] /= max_val
        
    return bonus

def gerar_memoria_reforco():
    memoria = {i: 0 for i in range(100)}
    
    previsoes = Previsao.objects.exclude(numeros_reais=None).order_by('-id')[:200]
    
    for p in previsoes:
        previstos = set(p.numeros_previstos)
        reais = set(p.numeros_reais)
        
        acertos = previstos & reais
        erros = previstos - reais
        
        for n in acertos:
            memoria[n] += 1
            
        for n in erros:
            memoria[n] -= 0.5
            
    return memoria

def normalizar_memoria(memoria):
    max_val = max(abs(v) for v in memoria.values()) or 1
    
    return {k:v / max_val for k, v in memoria.items()}