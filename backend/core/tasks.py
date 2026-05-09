import logging

from celery import shared_task  # type: ignore

from .models import Lista
from .services.previsao_pipeline import gerar_previsao_ml_pipeline

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def gerar_previsao_ml_task(self, limite=100):
    listas = list(
        Lista.objects.order_by("-id")
        .values_list("numeros", flat=True)[: int(limite)]
    )
    logger.info("gerar_previsao_ml_task: %s listas carregadas", len(listas))

    return gerar_previsao_ml_pipeline(listas, salvar=True)

