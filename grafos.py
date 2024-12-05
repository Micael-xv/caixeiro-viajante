import itertools
import networkx as nx
import matplotlib.pyplot as plt

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

def gerar_grafo_visual(cidades, grafo, rota_otima):
    G = nx.Graph()

    # Adicionando os nós (cidades) ao grafo
    G.add_nodes_from(cidades)

    # Adicionando as arestas com os pesos (distâncias)
    for cidade1 in grafo:
        for cidade2 in grafo[cidade1]:
            if grafo[cidade1][cidade2] is not None:
                G.add_edge(cidade1, cidade2, weight=grafo[cidade1][cidade2])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 8))

    # Desenhando o grafo
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray")

    # Adicionando as distâncias como rótulos nas arestas
    edge_labels = {(cidade1, cidade2): f"{grafo[cidade1][cidade2]}" for cidade1 in grafo for cidade2 in grafo[cidade1] if grafo[cidade1][cidade2] is not None}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    if rota_otima:
        for i in range(len(rota_otima) - 1):
            cidade1, cidade2 = rota_otima[i], rota_otima[i + 1]
            plt.plot([pos[cidade1][0], pos[cidade2][0]], [pos[cidade1][1], pos[cidade2][1]], color="red", lw=2)

    plt.title("Grafo das Cidades com a Melhor Rota")
    plt.show()

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
    gerar_grafo_visual(cidades, grafo, rota_otima)
else:
    print("Não foi possível encontrar uma rota válida entre as cidades.")
