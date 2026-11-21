import numpy as np

def criar_rng(seed: int) -> np.random.Generator:
    """Gerador aleatório único do projeto; todo código aleatório recebe este objeto."""
    return np.random.default_rng(seed)