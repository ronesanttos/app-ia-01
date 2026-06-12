from ..models import Previsao
from .ml_service import previsao_machine_learning, adicionar_ruido
from .previsao_service import prever_inteligente_v2
from .aprendizado_service import ajustar_por_historico
from ..utils import deduplicar_listas
import logging

logger = logging.getLogger(__name__)
    
def previsao_recente(tipo, previsao):
    ultimas = Previsao.objects.filter(tipo=tipo).order_by('-id')[:20]
    historico = [p.numeros_previstos for p in ultimas]
    return previsao in historico

def gerar_previsao_heuristica_pipeline(listas, salvar=True):
    listas_calc = deduplicar_listas(listas)
    resultado = prever_inteligente_v2(listas_calc)
    
    if "previsao" not in resultado: 
        return {
            "success": False,
            "erro": resultado.get("erro","Erro desconhecido")
            }
    
    previsao = resultado["previsao"]
    
    if not previsao:
        return {
            "erro": "Previsão vazia"
            }
    
    if previsao_recente("heuristica", previsao):
        return {
            "status": "duplicado_recente",
            "previsao": previsao
        }
        
    if salvar:
        Previsao.objects.create(
            tipo="heuristica",
            numeros_previstos=previsao
        )
    
    return {
        "success": True,
        "status": "ok",
        "data": {
            "previsao": previsao
        }
    }
    
def gerar_previsao_ml_pipeline(listas, salvar=True):
    listas_calc = deduplicar_listas(listas)
    resultado = previsao_machine_learning(listas_calc)
    
    if not resultado or "previsao" not in resultado:
        logger.warning("Erro no ML: %s", resultado)
        return {
            "success": False,
            "erro": resultado.get("erro","Erro desconhecido")
        }

    previsao = resultado["previsao"]
    previsao = ajustar_por_historico(previsao)
    previsao = adicionar_ruido(previsao)
    
    if not previsao:
        return {
            "erro": "Previsão vazia"
            }
    
    if previsao_recente("ml", previsao):
        return {
            "success": False,
            "status": "duplicado_recente",
            "data": {"previsao": previsao}
        }
        
    if salvar:
        try:
            Previsao.objects.create(
                tipo="ml",
                numeros_previstos=previsao,
                probabilidades=resultado.get("top_probabilidades", [])
            )
            logger.info("Previsão ML salva no banco.")
        except Exception as e:
            logger.exception("Erro ao salvar previsão ML: %s", e)

    return {
        "success": True,
        "status": "ok",
        "data": {
            "previsao": previsao,
            "probabilidades": resultado.get("top_probabilidades", [])
        }
    }




def gerar_previsao_heuristica_pipeline_15(listas, salvar=True):
    listas_calc = deduplicar_listas(listas)
    resultado = prever_inteligente_v2(listas_calc,tamanho_lista=15)
    
    if "previsao" not in resultado: 
        return {
            "success": False,
            "erro": resultado.get("erro","Erro desconhecido")
            }
    
    previsao = resultado["previsao"]
    
    if not previsao:
        return {
            "erro": "Previsão vazia"
            }
    
    if previsao_recente("heuristica", previsao):
        return {
            "status": "duplicado_recente",
            "previsao": previsao
        }
        
    if salvar:
        Previsao.objects.create(
            tipo="heuristica",
            numeros_previstos=previsao
        )
    
    return {
        "success": True,
        "status": "ok",
        "data": {
            "previsao": previsao
        }
    }