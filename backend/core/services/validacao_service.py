from ..models import Previsao

def validar_previsao(previsao_id, numeros_reais):
    try:
        previsao = Previsao.objects.get(id=previsao_id)
    except Previsao.DoesNotExist:
        return {"erro":"Previsão não encontrada"}
    
    previstos = set(previsao.numeros_previstos)
    reais = set(numeros_reais)
    data_previsao = previsao.criada_em
    
    acertos = len(previstos & reais)
    total = len(previstos)
    
    taxa_acerto = acertos / total if total > 0 else 0
    
    previsao.numeros_reais = numeros_reais
    previsao.acertos = acertos
    previsao.taxa_acerto = taxa_acerto
    previsao.acuracia = taxa_acerto
    previsao.save()
    
    return {
        "acertos": acertos,
        "total": total,
        "acuracia": taxa_acerto,
        "data_previsao": data_previsao
    }