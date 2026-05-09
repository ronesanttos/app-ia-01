from collections import Counter

def processar_listas(listas):
    todos_numeros = [num for lista in listas for num in lista]
    
    contagem = Counter(todos_numeros)
    
    nao_repete = [n for n, q in contagem.items() if q == 1]
    repete = [n for n, q in contagem.items() if q > 1]
    
    #qtd de numeros (ex:0 ate 99)
    universo = set(range(100))
    falta = list(universo - set(todos_numeros))
    
    return {
        "nao_repete": sorted(nao_repete),
        "repete": sorted(repete),
        "falta": sorted(falta),
    }
    
