from ..models import Lista, Previsao
from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from ..utils import gerar_heatmap, deduplicar_listas


def gerar_dashboard():
    previsoes = Previsao.objects.all()
    
    total = previsoes.count()
    acuracia_media = previsoes.aggregate(Avg('acuracia'))['acuracia__avg']
    
    top = previsoes.order_by('-acuracia')[:5]
    
    evolucao = (
        previsoes
        .annotate(data=TruncDate('criada_em'))
        .values('data')
        .annotate(media=Avg('acuracia'))
        .order_by('data')
    )
    
    por_tipo = (
        previsoes
        .values('tipo')
        .annotate(media=Avg('acuracia'), total=Count('id'))
    )
    
    listas = list(Lista.objects.values_list('numeros', flat=True)[:50])
    heatmap = gerar_heatmap(deduplicar_listas(listas), ordenar="frequencia")
    
    return {
        "resumo": {
            "total_previsoes": total,
            "acuracia_media": acuracia_media
        },
        "top_previsoes": [
            {"id": p.id, "tipo": p.tipo, "acuracia": p.acuracia}
            for p in top
        ],
        "evolucao": list(evolucao),
        "por_tipo": list(por_tipo),
        "heatmap": [
            {"numero": k, "frequencia": v}
            for k, v in heatmap.items()
        ],
        "top_numeros": top_numeros(heatmap)
    }
    
def top_numeros(heatmap,limite=20):
    ordenado = sorted(heatmap.items(), key=lambda x: x[1], reverse=True)
    
    return [
        {"numero": k, "frequencia": v}
        for k,v in ordenado[:limite]
    ]