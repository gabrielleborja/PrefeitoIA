from dataclasses import dataclass, fields
from pathlib import Path

import yaml

CAMINHO_PADRAO = Path(__file__).resolve().parents[2] / "config" / "default.yaml"

@dataclass(frozen=True)
class Params:
    # Doença
    beta0: float
    acoplamento_fome: float
    contagio_vizinhos: float
    duracao_imunidade: int
    p_notif_min: float
    p_notif_max: float
    decaimento_notif: float

    # Fome
    cresc_fome: float
    pessoas_por_cesta: float
    fome_retorno: float
    duracao_seguranca: int
    duracao_seguranca_dep: int

    # Orçamento e construções
    saldo_inicial: float
    arrecadacao_base: float
    peso_fome: float
    peso_saude: float
    preco_cesta: float
    preco_med: float
    custo_km: float
    base_obra: float
    obra_por_hab: float
    base_manut: float
    manut_por_hab: float

    # Regras 
    fome_max: float
    infectados_max: float
    turnos_max: int

    # Inicio
    bairros_infectados_iniciais: int
    infectados_iniciais_max: float
    fome_inicial_max: float


def carregar_params(caminho=CAMINHO_PADRAO, **substituicoes) -> Params:
    """Lê o YAML e devolve um Params.

    `substituicoes` troca valores sem editar o arquivo, pra usar na calibração:
        carregar_params(beta0=0.4)
    """
    with open(caminho, encoding="utf-8") as arquivo:
        dados = yaml.safe_load(arquivo)
    dados.update(substituicoes)

    esperados = {campo.name for campo in fields(Params)}
    faltando = esperados - dados.keys()
    sobrando = dados.keys() - esperados
    if faltando or sobrando:
        raise ValueError(
            f"Parâmetros faltando no YAML: {sorted(faltando)}; "
            f"parâmetros desconhecidos: {sorted(sobrando)}"
        )
    return Params(**dados)