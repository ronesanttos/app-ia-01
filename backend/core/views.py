from .models import Lista, Resultado, Previsao
from .serializers import ListaInputSerializer, ValidarPrevisaoSerializer

from .services.analise_service import processar_listas
from .services.previsao_pipeline import gerar_previsao_heuristica_pipeline, gerar_previsao_ml_pipeline
from .services.previsao_service import prever_com_aprendizado
from .services.ml_service import rodar_ml_em_background
from .services.validacao_service import validar_previsao
from .services.metricas_service import obter_metricas
from .services.dashboard_service import gerar_dashboard
from .services.historico_service import listar_historico
from .utils import normalizar_listas

from django.core.cache import cache
from django.utils import timezone
from rest_framework.viewsets import ViewSet #type:ignore
from rest_framework.response import Response#type:ignore
from rest_framework import status#type:ignore
from rest_framework.decorators import action#type:ignore
from rest_framework.authentication import SessionAuthentication  # type: ignore
from celery.result import AsyncResult  # type: ignore
import logging
import redis  # type: ignore
from django.conf import settings

from .auth import APIKeyAuthentication
from .tasks import gerar_previsao_ml_task

logger = logging.getLogger(__name__)

class ListaViewSet(ViewSet):
    authentication_classes = [APIKeyAuthentication, SessionAuthentication]

    # POST /api/listas/processar/
    @action(detail=False, methods=['post'])
    def processar(self,request):
        serializer = ListaInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        listas = normalizar_listas(serializer.validated_data['listas'])
        
        Lista.objects.bulk_create([
            Lista(numeros=l) for l in listas
        ])
       
        resultado = processar_listas(listas)
        
        return Response(resultado)


    # GET /api/listas/previsao/  retorna 1 previsao
    @action(detail=False, methods=['get'])
    def previsao(self,request):
        listas = list(
            Lista.objects.order_by('-id')
            .values_list('numeros',flat=True)[:100]
        )

        resultado = gerar_previsao_heuristica_pipeline(listas,salvar=False)  
        
        return Response(resultado)
    
    @action(detail=False, methods=['post'])
    def gerar_previsao(self, request):
        listas = list(
            Lista.objects.order_by('-id')
            .values_list('numeros', flat=True)[:100]
        )

        resultado = gerar_previsao_heuristica_pipeline(listas,salvar=True)
        
        return Response(resultado)
    
    # GET /api/listas/previsao_ml/ 
    @action(detail=False, methods=['get'])
    def previsao_ml(self,request):
        # Fail fast se o Redis não estiver acessível (evita travar a requisição)
        try:
            r = redis.Redis.from_url(
                settings.CELERY_BROKER_URL,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            r.ping()
        except Exception as e:
            logger.warning("Redis ping falhou ao enfileirar ML: %s", e)
            return Response(
                {"erro": "Redis indisponível. Suba o Redis para enfileirar a tarefa."},
                status=503,
            )

        try:
            task = gerar_previsao_ml_task.delay(100)
        except Exception as e:
            logger.warning("Não foi possível enfileirar task do ML: %s", e)
            return Response(
                {"erro": "Celery/Redis indisponível para enfileirar a tarefa."},
                status=503,
            )

        cache.set("ml_last_task_id", task.id, timeout=60 * 60)
        cache.set("ml_last_task_started_at", timezone.now().isoformat(), timeout=60 * 60)
        return Response({"status": "processando", "task_id": task.id})

    # GET /api/listas/previsao_ml_status/?task_id=...
    @action(detail=False, methods=["get"])
    def previsao_ml_status(self, request):
        task_id = request.query_params.get("task_id")
        if not task_id:
            return Response({"erro": "Envie task_id"}, status=400)

        try:
            r = redis.Redis.from_url(
                settings.CELERY_RESULT_BACKEND,
                socket_connect_timeout=1,
                socket_timeout=1,
            )
            r.ping()
        except Exception as e:
            logger.warning("Redis ping falhou ao consultar status: %s", e)
            ultima = Previsao.objects.filter(tipo="ml").order_by("-id").first()
            payload = {
                "task_id": task_id,
                "status": "UNAVAILABLE",
                "erro": "Redis indisponível para consultar status da task.",
            }
            if ultima:
                payload["ultima_previsao_salva"] = {
                    "id": ultima.id,
                    "numeros": ultima.numeros_previstos,
                    "criada_em": ultima.criada_em,
                }
            return Response(payload, status=503)

        result = AsyncResult(task_id)
        payload = {
            "task_id": task_id,
            "status": result.status,
        }

        ultima = Previsao.objects.filter(tipo="ml").order_by("-id").first()
        if ultima:
            payload["ultima_previsao_salva"] = {
                "id": ultima.id,
                "numeros": ultima.numeros_previstos,
                "criada_em": ultima.criada_em,
            }

        if result.successful():
            try:
                payload["result"] = result.result
            except Exception:
                payload["result"] = None
        elif result.failed():
            payload["error"] = str(result.result)

        return Response(payload)
    
    @action(detail=False, methods=['get'])
    def previsao_ml_preview(self,request):
        # Por padrão, reaproveita a última previsão ML já salva (sem recomputar).
        if request.query_params.get("force") not in ("1", "true", "yes", "on"):
            ultima = Previsao.objects.filter(tipo="ml").order_by("-id").first()
            if ultima:
                return Response(
                    {
                        "success": True,
                        "status": "ok",
                        "data": {
                            "previsao": ultima.numeros_previstos,
                            "probabilidades": ultima.probabilidades or [],
                        },
                        "source": "db",
                        "id": ultima.id,
                        "criada_em": ultima.criada_em,
                    }
                )

        listas = list(
            Lista.objects.order_by("-id")
            .values_list("numeros", flat=True)[:100]
        )

        resultado = gerar_previsao_ml_pipeline(listas, salvar=False)
        resultado["source"] = "compute"
        return Response(resultado)
        
    
    #retorna 10 previsoes
    @action(detail=False, methods=['get'])
    def previsoes(self, request):
        limit = int(request.query_params.get("limit", 20))
        previsao = Previsao.objects.order_by('-id')[:limit]
        
        return Response([
            {
                "id": p.id,
                "tipo": p.tipo,
                "numeros": p.numeros_previstos,
                "criada_em": p.criada_em
            }
            for p in previsao
        ])

    @action(detail=False, methods=['get'])
    def ultimas_listas(self, request):
        try:
            limite = int(request.query_params.get("limite", 6))
        except ValueError:
            limite = 6
        limite = max(1, min(limite, 50))

        rows = list(Lista.objects.order_by("-id")[:limite])
        if not rows:
            return Response({"erro": "Nenhuma lista cadastrada"}, status=404)

        listas_payload = [
            {"numeros": r.numeros, "criada_em": r.criada_em} for r in rows
        ]
        uniao = set()
        for r in rows:
            uniao.update(r.numeros)
        numeros_referencia = sorted(uniao)

        return Response(
            {
                "listas": listas_payload,
                "numeros_referencia": numeros_referencia,
                "limite": limite,
            }
        )

    @action(detail=False, methods=['get'])
    def metricas(self,request):
       return Response(obter_metricas())

    @action(detail=True, methods=['post'])
    def validar(self,request, pk=None):
        serializer = ValidarPrevisaoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        numeros_reais = serializer.validated_data["numeros"]
        
        resultado = validar_previsao(pk, numeros_reais)
        
        return Response(resultado)
    
    
    @action(detail=False, methods=['get'])
    def previsao_aprendizado(self, request):
        listas = list(
            Lista.objects.order_by('-id')
            .values_list('numeros', flat=True)[:100]
        )
        
        if not listas:
            return Response({"erro": "Sem dados"}, status=404)
        
        resultado = prever_com_aprendizado(listas)
        
        return Response(resultado)
        
    @action(detail=False, methods=['get'])
    def dashboard(self,request):
        return Response(gerar_dashboard())
    
    
    
    @action(detail=False, methods=['get'])
    def historico(self,request):
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 1))
        tipo = request.query_params.get('tipo')
        
        return Response(listar_historico(page,limit,tipo))
    
    
    
  