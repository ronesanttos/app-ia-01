from ..models import Previsao
from django.db.models import F

def listar_historico(page=1,limit=10, tipo=None, ordenar_por="acuracia"):
    
    try:
        page = int(page)
        limit = int(limit)
    except:
        page = 1
        limit = 10
        
    limit = min(limit,50)
    inicio = (page - 1) * limit

    queryset = Previsao.objects.all()

    if tipo:
        queryset = queryset.filter(tipo=tipo)
        
    if ordenar_por == "acuracia":
        queryset = queryset.order_by(F('acuracia').desc(nulls_last=True),'-criada_em')
        
    total = queryset.count()

    previsoes = queryset[inicio:inicio + limit]

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "ordenar": ordenar_por,
        "results": [
            {
                "id": p.id,
                "tipo": p.tipo,
                "numeros_previstos": p.numeros_previstos,
                "numeros_reais": p.numeros_reais,
                "acuracia": p.acuracia,
                "data": p.criada_em
            }
            for p in previsoes
        ]
    }