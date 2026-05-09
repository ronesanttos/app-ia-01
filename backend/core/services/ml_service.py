import os
from pathlib import Path
import joblib #type:ignore
import random

from ..ml import (gerar_dataset,treinar_modelo,prever_com_modelo)

from ..models import Previsao

MODEL_PATH = Path(__file__).resolve().parents[2] / "modelo.pkl"

def obter_modelo(listas,retrain=False):
    if MODEL_PATH.exists() and not retrain:
        return joblib.load(MODEL_PATH)
    
    X,y = gerar_dataset(listas)
    
    if X is None or len(X) < 5:
        return None
    
    modelos = treinar_modelo(X,y)
    joblib.dump(modelos, MODEL_PATH)
    
    return modelos
    
def previsao_machine_learning(listas,retrain=False):
    modelos = obter_modelo(listas, retrain)
    
    if not modelos:
        return {"erro": "Modelo indisponível"}
    
    return prever_com_modelo(modelos,listas)

def adicionar_ruido(previsao, intensidade=0.2):
    novos = previsao.copy()
    
    for i in range(len(novos)):
        if random.random() < intensidade:
            novos[i] = random.randint(0,99)
        
    return list(set(novos))[:len(previsao)]

def rodar_ml_em_background(listas):
    from .previsao_pipeline import gerar_previsao_ml_pipeline
    gerar_previsao_ml_pipeline(listas)
    