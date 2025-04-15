import unittest
import math
import sys
import os

class TestCalculadoraDesconto(unittest.TestCase):
    """
    Testes automatizados para validar a calculadora de desconto do SuperCalc.
    Estes testes verificam se os cálculos de desconto simples, composto e progressivo estão corretos.
    """
    
    def test_desconto_simples(self):
        """
        Testa o cálculo de desconto simples com diferentes valores de entrada.
        Fórmula: D = V * (p/100), onde:
        - D = valor do desconto
        - V = valor original
        - p = percentual de desconto
        """
        # Caso 1: Valores inteiros
        valor_original = 1000
        percentual = 10
        desconto_esperado = valor_original * (percentual / 100)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 100.0)
        self.assertEqual(valor_final_esperado, 900.0)
        
        # Caso 2: Valores decimais
        valor_original = 1500.50
        percentual = 15.5
        desconto_esperado = valor_original * (percentual / 100)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertAlmostEqual(desconto_esperado, 232.58, delta=0.01)
        self.assertAlmostEqual(valor_final_esperado, 1267.92, delta=0.01)
        
        # Caso 3: Percentual zero
        valor_original = 2000
        percentual = 0
        desconto_esperado = valor_original * (percentual / 100)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 0.0)
        self.assertEqual(valor_final_esperado, valor_original)
    
    def test_desconto_progressivo(self):
        """
        Testa o cálculo de desconto progressivo com diferentes valores de entrada.
        Desconto progressivo: aplica percentuais diferentes conforme o valor da compra.
        """
        # Função para calcular desconto progressivo
        def calcular_desconto_progressivo(valor):
            if valor < 100:
                percentual = 5
            elif valor < 500:
                percentual = 10
            elif valor < 1000:
                percentual = 15
            else:
                percentual = 20
            
            return valor * (percentual / 100)
        
        # Caso 1: Valor baixo (< 100)
        valor_original = 80
        desconto_esperado = calcular_desconto_progressivo(valor_original)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 4.0)  # 5% de 80
        self.assertEqual(valor_final_esperado, 76.0)
        
        # Caso 2: Valor médio-baixo (100-499)
        valor_original = 300
        desconto_esperado = calcular_desconto_progressivo(valor_original)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 30.0)  # 10% de 300
        self.assertEqual(valor_final_esperado, 270.0)
        
        # Caso 3: Valor médio-alto (500-999)
        valor_original = 750
        desconto_esperado = calcular_desconto_progressivo(valor_original)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 112.5)  # 15% de 750
        self.assertEqual(valor_final_esperado, 637.5)
        
        # Caso 4: Valor alto (>= 1000)
        valor_original = 2000
        desconto_esperado = calcular_desconto_progressivo(valor_original)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 400.0)  # 20% de 2000
        self.assertEqual(valor_final_esperado, 1600.0)
    
    def test_desconto_por_cupom(self):
        """
        Testa o cálculo de desconto aplicado por cupom promocional.
        """
        # Função para calcular desconto por cupom
        def calcular_desconto_cupom(valor, cupom):
            cupons = {
                'PROMO10': 10,
                'PROMO20': 20,
                'PROMO30': 30,
                'SUPER50': 50
            }
            
            if cupom in cupons:
                percentual = cupons[cupom]
                return valor * (percentual / 100)
            return 0
        
        # Caso 1: Cupom válido PROMO10
        valor_original = 1000
        cupom = 'PROMO10'
        desconto_esperado = calcular_desconto_cupom(valor_original, cupom)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 100.0)  # 10% de 1000
        self.assertEqual(valor_final_esperado, 900.0)
        
        # Caso 2: Cupom válido SUPER50
        valor_original = 1000
        cupom = 'SUPER50'
        desconto_esperado = calcular_desconto_cupom(valor_original, cupom)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 500.0)  # 50% de 1000
        self.assertEqual(valor_final_esperado, 500.0)
        
        # Caso 3: Cupom inválido
        valor_original = 1000
        cupom = 'INVALIDO'
        desconto_esperado = calcular_desconto_cupom(valor_original, cupom)
        valor_final_esperado = valor_original - desconto_esperado
        
        self.assertEqual(desconto_esperado, 0.0)  # Cupom inválido, sem desconto
        self.assertEqual(valor_final_esperado, valor_original)


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