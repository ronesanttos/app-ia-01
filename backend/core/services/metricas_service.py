from ..models import Previsao
from django.db.models import Avg, F, FloatField, Value
from django.db.models.functions import Coalesce

def obter_metricas():
    total = Previsao.objects.count()

    acuracia_media = Previsao.objects.aggregate(
        media=Avg(Coalesce("acuracia", "taxa_acerto", output_field=FloatField()))
    )["media"]

    melhores = (
        Previsao.objects.annotate(
            _score=Coalesce("acuracia", "taxa_acerto", Value(-1.0), output_field=FloatField())
        )
        .order_by(F("_score").desc(nulls_last=True), "-id")[:5]
    )

    return {
        "total_previsoes": total,
        "acuracia": acuracia_media,
        "top_5": [
            {
                "id": p.id,
                "tipo": p.tipo,
                "acuracia": p.acuracia,
                "taxa_acerto": p.taxa_acerto,
            }
            for p in melhores
        ],
    }
    
    