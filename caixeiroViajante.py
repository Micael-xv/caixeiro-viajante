import itertools

def inserir_cidades():
    num_cidades = int(input("Quantas cidades? "))
    cidades = []
    for i in range(num_cidades):
        cidade = input(f"Nome da cidade {i+1}: ")
        cidades.append(cidade)
    return cidades

def inserir_distancias(cidades):
    num_cidades = len(cidades)
    distancias = {cidade: {} for cidade in cidades}

    for i in range(num_cidades):
        for j in range(i + 1, num_cidades):
            distancia = input(f"Distância de {cidades[i]} para {cidades[j]} (ou 'inf' se não se conectam): ")
            if distancia == "inf":
                distancias[cidades[i]][cidades[j]] = None
                distancias[cidades[j]][cidades[i]] = None
            else:
                distancias[cidades[i]][cidades[j]] = float(distancia)
                distancias[cidades[j]][cidades[i]] = float(distancia)

    return distancias

def calcular_custo(rota, grafo):
    custo_total = 0
    for i in range(len(rota) - 1):
        if grafo[rota[i]][rota[i + 1]] is None:
            return float('inf')  # Retorna custo inf p/ indicar que aquela rota não é válida
        custo_total += grafo[rota[i]][rota[i + 1]]
    # Verifica o retorno à cidade inicial
    if grafo[rota[-1]][rota[0]] is None:
        return float('inf')
    custo_total += grafo[rota[-1]][rota[0]]
    return custo_total

def encontrar_rota_otima(cidades, grafo):
    rota_otima = None
    custo_minimo = float('inf')

    for rota in itertools.permutations(cidades[1:]):
        rota_completa = [cidades[0]] + list(rota)
        custo = calcular_custo(rota_completa, grafo)
        if custo < custo_minimo:
            custo_minimo = custo
            rota_otima = rota_completa

    return rota_otima, custo_minimo

# Inserir as cidades
cidades = inserir_cidades()

# Inserir as distâncias entre as cidades
grafo = inserir_distancias(cidades)

# Encontrar a melhor rota testando as possibilidades
rota_otima, custo_minimo = encontrar_rota_otima(cidades, grafo)

# Verificar se uma rota foi encontrada
if rota_otima:
    # Adicionar a cidade inicial ao final
    rota_otima.append(rota_otima[0])
    print(f"Melhor rota: {' -> '.join(rota_otima)} com custo {custo_minimo}")
else:
    print("Não foi possível encontrar uma rota válida entre as cidades.")