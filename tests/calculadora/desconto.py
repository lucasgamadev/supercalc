"""
Módulo de lógica para cálculo de desconto.
"""
from typing import Optional

def desconto_simples(valor: float, percentual: float) -> float:
    if valor < 0:
        raise ValueError("O valor original não pode ser negativo.")
    if percentual < 0 or percentual > 100:
        raise ValueError("O percentual de desconto deve estar entre 0 e 100.")
    return valor * (percentual / 100)

def desconto_progressivo(valor: float) -> float:
    if valor < 0:
        raise ValueError("O valor original não pode ser negativo.")
    if valor < 100:
        percentual = 5
    elif valor < 500:
        percentual = 10
    elif valor < 1000:
        percentual = 15
    else:
        percentual = 20
    return valor * (percentual / 100)

def desconto_cupom(valor: float, cupom: Optional[str]) -> float:
    if valor < 0:
        raise ValueError("O valor original não pode ser negativo.")
    cupons = {
        'PROMO10': 10,
        'PROMO20': 20,
        'PROMO30': 30,
        'SUPER50': 50
    }
    percentual = cupons.get(cupom, 0)
    return valor * (percentual / 100)
