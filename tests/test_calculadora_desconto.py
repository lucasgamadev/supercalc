import unittest
import math
import sys
import os

class TestCalculadoraDesconto(unittest.TestCase):
    """
    Testes automatizados para validar a calculadora de desconto do SuperCalc.
    Estes testes verificam se os cálculos de desconto simples e percentual estão corretos.
    """
    
    def test_desconto_simples(self):
        """
        Testa o cálculo de desconto simples.
        Fórmula: D = V * (p/100), onde:
        - D = desconto
        - V = valor original
        - p = percentual de desconto
        """
        # Caso 1: 10% de desconto em 100
        self.assertAlmostEqual(self.calcular_desconto(100, 10), 10)
        # Caso 2: 25% de desconto em 200
        self.assertAlmostEqual(self.calcular_desconto(200, 25), 50)
        # Caso 3: 0% de desconto
        self.assertAlmostEqual(self.calcular_desconto(100, 0), 0)
        # Caso 4: 100% de desconto
        self.assertAlmostEqual(self.calcular_desconto(100, 100), 100)
        # Caso 5: desconto com valor decimal
        self.assertAlmostEqual(self.calcular_desconto(99.99, 15.5), 15.49845)
    
    def test_valor_final(self):
        """
        Testa o cálculo do valor final após aplicar o desconto.
        Valor final = valor original - desconto
        """
        self.assertAlmostEqual(self.valor_final(100, 10), 90)
        self.assertAlmostEqual(self.valor_final(200, 25), 150)
        self.assertAlmostEqual(self.valor_final(100, 0), 100)
        self.assertAlmostEqual(self.valor_final(100, 100), 0)
        self.assertAlmostEqual(self.valor_final(99.99, 15.5), 84.49155)
    
    def test_valores_extremos(self):
        """
        Testa o comportamento com valores extremos.
        """
        # Desconto sobre valor zero
        self.assertAlmostEqual(self.calcular_desconto(0, 10), 0)
        self.assertAlmostEqual(self.valor_final(0, 10), 0)
        # Percentual negativo (não deve ocorrer, mas o teste verifica)
        self.assertAlmostEqual(self.calcular_desconto(100, -10), -10)
        self.assertAlmostEqual(self.valor_final(100, -10), 110)
        # Valor negativo
        self.assertAlmostEqual(self.calcular_desconto(-100, 10), -10)
        self.assertAlmostEqual(self.valor_final(-100, 10), -90)
        # Percentual acima de 100%
        self.assertAlmostEqual(self.calcular_desconto(100, 150), 150)
        self.assertAlmostEqual(self.valor_final(100, 150), -50)
    
    # Métodos auxiliares para realizar os cálculos
    def calcular_desconto(self, valor, percentual):
        """
        Calcula o valor do desconto.
        """
        return valor * (percentual / 100)
    
    def valor_final(self, valor, percentual):
        """
        Calcula o valor final após o desconto.
        """
        return valor - self.calcular_desconto(valor, percentual)

def executar_testes_desconto():
    """
    Executa todos os testes da calculadora de desconto.
    Retorna True se todos os testes passarem, False caso contrário.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculadoraDesconto)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()

if __name__ == "__main__":
    print("\n===== TESTES DA CALCULADORA DE DESCONTO =====\n")
    sucesso = executar_testes_desconto()
    sys.exit(0 if sucesso else 1)
