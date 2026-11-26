# cidade: bairros, regiões, vizinhança e distâncias
import json
import math
from dataclasses import dataclass

import networkx as nx
import numpy as np

ID_PREFEITURA = "P"


@dataclass(frozen=True)
class Cidade:
    ids: list           # ids dos bairros(sem a prefeitura)
    regioes: list       # nomes das regiões
    regiao: np.ndarray  # índice da região de cada bairro
    pop: np.ndarray     # população de cada bairro
    A: np.ndarray       # (n, n) 1 se dois bairros são vizinhos (a prefeitura não conta)
    D: np.ndarray       # (n+1, n+1) menor distância entre nós; o último índice é a prefeitura
    mediana: np.ndarray # (n_regioes,) índice do bairro onde ficam as instalações de cada região
    grafo: nx.Graph

    @property
    def n(self) -> int:
        """Número de bairros"""
        return len(self.ids)

    @property
    def prefeitura(self) -> int:
        """Índice da prefeitura na matriz D"""
        return len(self.ids)


def montar_cidade(grafo: nx.Graph) -> Cidade:
    """Monta a Cidade a partir do grafo, com nó da prefeitura, dos bairros com os
    atributos 'regiao' e 'pop', e arestas com o atributo 'weight' (distância)
    """
    # A ordem dos bairros vale para todos os arrays
    ids = [no for no in grafo.nodes if no != ID_PREFEITURA]
    indice = {bairro: i for i, bairro in enumerate(ids)}
    n = len(ids)

    regioes = sorted({grafo.nodes[b]["regiao"] for b in ids})
    regiao = np.array([regioes.index(grafo.nodes[b]["regiao"]) for b in ids])
    pop = np.array([float(grafo.nodes[b]["pop"]) for b in ids])

    # dois bairros ligados apenas pela prefeitura não são vizinhos
    A = np.zeros((n, n))
    for u, v in grafo.edges:
        if u in indice and v in indice:
            A[indice[u], indice[v]] = 1.0
            A[indice[v], indice[u]] = 1.0

    # Menores distâncias entre todos os nós; a prefeitura fica no último índice
    ordem = ids + [ID_PREFEITURA]
    distancias = dict(nx.all_pairs_dijkstra_path_length(grafo, weight="weight"))
    D = np.array([[distancias[a][b] for b in ordem] for a in ordem])

    # Mediana de cada região: o bairro com a menor soma de distâncias aos outros da região
    mediana = np.empty(len(regioes), dtype=int)
    for r in range(len(regioes)):
        membros = np.flatnonzero(regiao == r)
        somas = D[np.ix_(membros, membros)].sum(axis=1)
        mediana[r] = membros[np.argmin(somas)]

    return Cidade(ids, regioes, regiao, pop, A, D, mediana, grafo)

