import pytest
from tests.calculadora import desconto

import math

@pytest.mark.parametrize("valor, percentual, esperado", [
    (1000, 10, 100.0),
    (1500.50, 15.5, 232.5775),
    (2000, 0, 0.0),
    (0, 10, 0.0),
])
def test_desconto_simples(valor, percentual, esperado):
    resultado = desconto.desconto_simples(valor, percentual)
    assert math.isclose(resultado, esperado, rel_tol=1e-4)

@pytest.mark.parametrize("valor, percentual_invalido", [
    (1000, -5),
    (1000, 120),
    (-100, 10),
])
def test_desconto_simples_erros(valor, percentual_invalido):
    with pytest.raises(ValueError):
        desconto.desconto_simples(valor, percentual_invalido)

@pytest.mark.parametrize("valor, desconto_esperado", [
    (80, 4.0),      # 5%
    (300, 30.0),    # 10%
    (750, 112.5),   # 15%
    (2000, 400.0),  # 20%
])
def test_desconto_progressivo(valor, desconto_esperado):
    resultado = desconto.desconto_progressivo(valor)
    assert math.isclose(resultado, desconto_esperado, rel_tol=1e-4)

@pytest.mark.parametrize("valor", [-1, -100])
def test_desconto_progressivo_valor_negativo(valor):
    with pytest.raises(ValueError):
        desconto.desconto_progressivo(valor)

@pytest.mark.parametrize("valor, cupom, esperado", [
    (1000, 'PROMO10', 100.0),
    (1000, 'SUPER50', 500.0),
    (1000, 'INVALIDO', 0.0),
    (0, 'PROMO10', 0.0),
])
def test_desconto_cupom(valor, cupom, esperado):
    resultado = desconto.desconto_cupom(valor, cupom)
    assert math.isclose(resultado, esperado, rel_tol=1e-4)

@pytest.mark.parametrize("valor", [-1, -100])
def test_desconto_cupom_valor_negativo(valor):
    with pytest.raises(ValueError):
        desconto.desconto_cupom(valor, 'PROMO10')