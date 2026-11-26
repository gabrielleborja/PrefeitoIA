# tudo o que muda a cada turno (um valor por bairro)
from dataclasses import dataclass

import numpy as np

from .cidade import Cidade
from .params import Params


@dataclass
class CityState:
    S: np.ndarray           
    I: np.ndarray           
    imunes: np.ndarray       
    fome: np.ndarray       
    seguranca: np.ndarray  
    notificados: np.ndarray  
    deposito: np.ndarray     
    posto: np.ndarray        
    saldo: float
    turno: int
    params: Params           # imutável mas o clone pode trocar 

    def clone(self, params: Params = None) -> "CityState":
        """Cópia independente do estado.
        """

        return CityState(
            S=self.S.copy(),
            I=self.I.copy(),
            imunes=self.imunes.copy(),
            fome=self.fome.copy(),
            seguranca=self.seguranca.copy(),
            notificados=self.notificados.copy(),
            deposito=self.deposito.copy(),
            posto=self.posto.copy(),
            saldo=self.saldo,
            turno=self.turno,
            params=self.params if params is None else params,
        )


def estado_inicial(cidade: Cidade, params: Params, rng: np.random.Generator) -> CityState:
    """Cenário de caos sorteado a partir do gerador. Mesma seed, mesmo cenário"""
    n = cidade.n

    # Sorteio de infectados em alguns bairros, até uma fração da população de cada um.
    I = np.zeros(n)
    k = min(params.bairros_infectados_iniciais, n)
    sorteados = rng.choice(n, size=k, replace=False)
    I[sorteados] = rng.uniform(0.01, params.infectados_iniciais_max, size=k) * cidade.pop[sorteados]

    return CityState(
        S=cidade.pop - I,
        I=I,
        imunes=np.zeros((n, params.duracao_imunidade)),
        fome=rng.uniform(0.0, params.fome_inicial_max, size=n),
        seguranca=np.zeros(n, dtype=int),
        notificados=np.zeros(n),
        deposito=np.zeros(len(cidade.regioes), dtype=bool),
        posto=np.zeros(len(cidade.regioes), dtype=bool),
        saldo=float(params.saldo_inicial),
        turno=0,
        params=params,
    )