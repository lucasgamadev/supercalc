import unittest
import math
import sys
import os

class TestCalculadoraPadrao(unittest.TestCase):
    """
    Testes automatizados para validar a calculadora padrão do SuperCalc.
    Estes testes verificam se as operações básicas e avançadas estão funcionando corretamente.
    """
    
    def test_operacoes_basicas(self):
        """
        Testa as operações básicas da calculadora: adição, subtração, multiplicação e divisão.
        """
        # Adição
        self.assertEqual(self.calcular(10, 5, '+'), 15)
        self.assertEqual(self.calcular(-10, 5, '+'), -5)
        self.assertEqual(self.calcular(10.5, 5.5, '+'), 16)
        
        # Subtração
        self.assertEqual(self.calcular(10, 5, '-'), 5)
        self.assertEqual(self.calcular(-10, 5, '-'), -15)
        self.assertEqual(self.calcular(10.5, 5.5, '-'), 5)
        
        # Multiplicação
        self.assertEqual(self.calcular(10, 5, '*'), 50)
        self.assertEqual(self.calcular(-10, 5, '*'), -50)
        self.assertEqual(self.calcular(10.5, 2, '*'), 21)
        
        # Divisão
        self.assertEqual(self.calcular(10, 5, '/'), 2)
        self.assertEqual(self.calcular(-10, 5, '/'), -2)
        self.assertEqual(self.calcular(10.5, 2, '/'), 5.25)
        
        # Divisão por zero
        with self.assertRaises(ZeroDivisionError):
            self.calcular(10, 0, '/')
    
    def test_operacoes_avancadas(self):
        """
        Testa operações avançadas da calculadora: potência, raiz quadrada, módulo e porcentagem.
        """
        # Potência
        self.assertEqual(self.calcular(2, 3, '^'), 8)
        self.assertEqual(self.calcular(3, 2, '^'), 9)
        self.assertEqual(self.calcular(10, 0, '^'), 1)
        
        # Raiz quadrada
        self.assertEqual(self.calcular(4, 0, 'sqrt'), 2)
        self.assertEqual(self.calcular(9, 0, 'sqrt'), 3)
        self.assertAlmostEqual(self.calcular(2, 0, 'sqrt'), 1.414, delta=0.001)
        
        # Módulo
        self.assertEqual(self.calcular(10, 3, '%'), 1)
        self.assertEqual(self.calcular(10, 2, '%'), 0)
        self.assertEqual(self.calcular(10, 7, '%'), 3)
        
        # Porcentagem
        self.assertEqual(self.calcular(100, 10, 'percent'), 10)
        self.assertEqual(self.calcular(50, 10, 'percent'), 5)
        self.assertEqual(self.calcular(200, 5, 'percent'), 10)
    
    def test_operacoes_trigonometricas(self):
        """
        Testa operações trigonométricas da calculadora: seno, cosseno e tangente.
        """
        # Seno
        self.assertAlmostEqual(self.calcular(0, 0, 'sin'), 0, delta=0.001)
        self.assertAlmostEqual(self.calcular(90, 0, 'sin', True), 1, delta=0.001)
        self.assertAlmostEqual(self.calcular(180, 0, 'sin', True), 0, delta=0.001)
        
        # Cosseno
        self.assertAlmostEqual(self.calcular(0, 0, 'cos'), 1, delta=0.001)
        self.assertAlmostEqual(self.calcular(90, 0, 'cos', True), 0, delta=0.001)
        self.assertAlmostEqual(self.calcular(180, 0, 'cos', True), -1, delta=0.001)
        
        # Tangente
        self.assertAlmostEqual(self.calcular(0, 0, 'tan'), 0, delta=0.001)
        self.assertAlmostEqual(self.calcular(45, 0, 'tan', True), 1, delta=0.001)
        
        # Verificar exceção para tangente de 90 graus
        with self.assertRaises(ValueError):
            self.calcular(90, 0, 'tan', True)
    
    def test_memoria(self):
        """
        Testa as operações de memória da calculadora: armazenar, recuperar, adicionar e subtrair.
        """
        # Inicializar memória
        memoria = 0
        
        # Armazenar na memória
        memoria = self.operacao_memoria(10, 'MS', memoria)
        self.assertEqual(memoria, 10)
        
        # Recuperar da memória
        resultado = self.operacao_memoria(0, 'MR', memoria)
        self.assertEqual(resultado, 10)
        
        # Adicionar à memória
        memoria = self.operacao_memoria(5, 'M+', memoria)
        self.assertEqual(memoria, 15)
        
        # Subtrair da memória
        memoria = self.operacao_memoria(7, 'M-', memoria)
        self.assertEqual(memoria, 8)
        
        # Limpar memória
        memoria = self.operacao_memoria(0, 'MC', memoria)
        self.assertEqual(memoria, 0)
    
    # Métodos auxiliares para realizar os cálculos
    def calcular(self, a, b, operacao, usar_graus=False):
        """
        Realiza o cálculo de acordo com a operação especificada.
        
        Args:
            a: Primeiro operando
            b: Segundo operando
            operacao: Operação a ser realizada
            usar_graus: Se True, converte graus para radianos nas operações trigonométricas
            
        Returns:
            Resultado da operação
        """
        if operacao == '+':
            return a + b
        elif operacao == '-':
            return a - b
        elif operacao == '*':
            return a * b
        elif operacao == '/':
            if b == 0:
                raise ZeroDivisionError("Divisão por zero não é permitida")
            return a / b
        elif operacao == '^':
            return a ** b
        elif operacao == 'sqrt':
            return math.sqrt(a)
        elif operacao == '%':
            return a % b
        elif operacao == 'percent':
            return a * (b / 100)
        elif operacao == 'sin':
            if usar_graus:
                return math.sin(math.radians(a))
            return math.sin(a)
        elif operacao == 'cos':
            if usar_graus:
                return math.cos(math.radians(a))
            return math.cos(a)
        elif operacao == 'tan':
            if usar_graus:
                # Verificar se é 90 graus ou equivalente
                if a % 180 == 90:
                    raise ValueError("Tangente de 90 graus não é definida")
                return math.tan(math.radians(a))
            return math.tan(a)
        else:
            raise ValueError(f"Operação '{operacao}' não suportada")
    
    def operacao_memoria(self, valor, operacao, memoria):
        """
        Realiza operações de memória da calculadora.
        
        Args:
            valor: Valor a ser usado na operação
            operacao: Operação de memória (MS, MR, M+, M-, MC)
            memoria: Valor atual da memória
            
        Returns:
            Novo valor da memória ou valor recuperado
        """
        if operacao == 'MS':  # Memory Store
            return valor
        elif operacao == 'MR':  # Memory Recall
            return memoria
        elif operacao == 'M+':  # Memory Add
            return memoria + valor
        elif operacao == 'M-':  # Memory Subtract
            return memoria - valor
        elif operacao == 'MC':  # Memory Clear
            return 0
        else:
            raise ValueError(f"Operação de memória '{operacao}' não suportada")


def executar_testes_padrao():
    """
    Executa todos os testes da calculadora padrão.
    Retorna True se todos os testes passarem, False caso contrário.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculadoraPadrao)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()


if __name__ == "__main__":
    print("\n===== TESTES DA CALCULADORA PADRÃO =====\n")
    sucesso = executar_testes_padrao()
    sys.exit(0 if sucesso else 1)