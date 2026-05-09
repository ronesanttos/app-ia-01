


numeros =   '''

obs : Subir o Redis de verdade:
Abra/inicie o Docker Desktop e confirme que docker info funciona.
Na pasta backend/, rode docker compose up -d (sobe Redis + worker Celery na imagem Linux).
Worker só no PC (Windows): py -m celery -A project worker -l info --pool=solo
GET /api/listas/previsao_ml/ → pegar task_id
GET /api/listas/previsao_ml_status/?task_id=... → ver concluir.
'''

# 1. Transforma a string em uma lista de números individuais
lista_completa = [str(int(n)) for n in numeros.split()]

# 2. Cria os grupos de 10 e junta-os com vírgula
linhas_formatadas = []
for i in range(0, len(lista_completa), 10):
    # Pega uma fatia (slice) de 10 números e junta com vírgula
    grupo = ",".join(lista_completa[i:i+10])
    linhas_formatadas.append(grupo)

# 3. Junta os grupos com uma quebra de linha (\n)
resultado_final = ",\n".join(linhas_formatadas)

print(resultado_final)


'''
frontend/frontend/ npm run dev
'''


'''
Melhores resultados 
id 28 = [4, 68, 45, 76, 7, 67, 96, 59, 85, 17]
id 26 = [4, 68, 7, 76, 45, 67, 85, 96, 59, 17]
id 24 = [7, 4, 76, 85, 68, 96, 45, 83, 70, 59]
id 22 = [7, 4, 76, 85, 96, 68, 70, 59, 41, 45]
id 20 = [33, 93, 96, 0, 5, 60, 81, 99, 16, 80]
id 19 = [7, 4, 96, 41, 76, 85, 83, 68, 70, 59]
id 13 = [27, 33, 60, 96, 0, 93, 99, 5, 81, 16]
id 5 =  [33, 93, 96, 0, 5, 60, 81, 99, 16, 80]
id 15 = [96, 41, 7, 60, 70, 83, 92, 68, 51, 31]
id 14 = [96, 41, 60, 51, 85, 7, 93, 92, 83, 68]
id 12 = [96, 41, 60, 51, 85, 7, 93, 92, 83, 68, 59, 31, 17, 6, 3]
id 10 = [96, 60, 51, 41, 7, 68, 85, 59, 93, 92, 83, 17, 6, 53, 31, 76, 45, 62, 3, 73]
id 9 = [96, 60, 51, 41, 7, 68, 85, 59, 93, 92, 83, 17, 6, 53, 31]

40,88,41,21,81,78,42,99,20,16,
0,55,87,96,27,16,3543,81,79,47,
43,49,90,19,66,60,56,78,16,1,
22,15,65,41,60,58,27,40,8,19,
56,19,0,83,39,36,16,29,99



Na próxima sessão, a primeira coisa é só confirmar o worker Celery está estável e então retestar previsao_ml_status até SUCCESS — aí seguimos para o frontend.


'''
