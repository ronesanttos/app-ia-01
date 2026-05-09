from collections import Counter
from itertools import combinations

def deduplicar_lista(lista):
    """
    Remove duplicados preservando a ordem.
    Usado para cálculos/pipelines sem alterar o payload original armazenado.
    """
    if not lista:
        return []
    return list(dict.fromkeys(lista))

def deduplicar_listas(listas):
    if not listas:
        return []
    return [deduplicar_lista(l) for l in listas]


def detectar_padroes(listas):
    pares = []
    for lista in listas:
       lista_unica = sorted(set(lista)) #remover repetidos
       pares.extend(combinations(lista_unica,2))
        
    contagem = Counter(pares)
    return dict(sorted(contagem.items(), key=lambda x: x[1], reverse=True))
    
def gerar_heatmap(listas,minimo=0,maximo=99, ordenar="numero"):
    from collections import Counter
    
    todos = [num for lista in listas for num in lista]
    contagem = Counter(todos)
    
    heatmap = {i: contagem.get(i,0) for i in range(minimo, maximo + 1)}
    
    if ordenar == "frequencia":
        return dict(sorted(heatmap.items(), key=lambda x: x[1], reverse=True))
    
    return dict(sorted(heatmap.items(), key=lambda x: x[0]))



def calcular_frequencia(listas): 
    todos_numeros = [num for lista in listas for num in lista] 
    frequencia = Counter(todos_numeros) 
    
    # ordena do mais frequente para o menos frequente 
    frequencia_ordenada = dict(sorted(frequencia.items(), key=lambda x: x[1], reverse=True)) 
    
    return frequencia_ordenada

def score_frequencia(frequencia):
    total = sum(frequencia.values())
    return {k: v / total for k, v in frequencia.items()}

def score_recencia(listas, janela=10):
    recentes = listas[-janela:]

    numeros = [num for lista in recentes for num in lista]

    contagem = Counter(numeros)
    total = sum(contagem.values())

    return {k: v / total for k, v in contagem.items()}

def score_padroes(listas):
    pares = detectar_padroes(listas)

    score = {}

    for (a, b), freq in pares.items():
        score[a] = score.get(a, 0) + freq
        score[b] = score.get(b, 0) + freq

    total = sum(score.values()) or 1

    return {k: v / total for k, v in score.items()}

def calcular_score_final(listas):
    # Para cálculos, tratamos duplicados como 1 ocorrência por lista
    listas = deduplicar_listas(listas)
    freq = calcular_frequencia(listas)

    s_freq = score_frequencia(freq)
    s_rec = score_recencia(listas)
    s_pad = score_padroes(listas)

    todos_numeros = set(range(0, 100))

    score_final = {}

    for num in todos_numeros:
        score_final[num] = (
            s_freq.get(num, 0) * 0.5 +
            s_rec.get(num, 0) * 0.3 +
            s_pad.get(num, 0) * 0.2
        )

    return dict(sorted(score_final.items(), key=lambda x: x[1], reverse=True))

def normalizar_listas(listas):
    novas = []
    
    for l in listas:
        if len(l) > 10:
            for i in range(0, len(l), 10):
                novas.append(l[i:i+10])
                
        else:
            novas.append(l)
            
    return novas

def calcular_peso_previsao(previsao):
    if previsao.acuracia is None:
        return 1
    
    return 0.5 + previsao.acuracia



