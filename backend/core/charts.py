import matplotlib.pyplot as plt #type:ignore

def plotar_heatmap(heatmap):
    numeros = list(heatmap.keys())
    valores = list(heatmap.values())
    
    plt.figure()
    plt.bar(numeros, valores)
    plt.xlabel("Números")
    plt.ylabel("Frequência")
    plt.title("Heatmap de Frequência")
    plt.show()