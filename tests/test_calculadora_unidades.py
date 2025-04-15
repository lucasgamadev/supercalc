import unittest
import math
import sys
import os

class TestCalculadoraUnidades(unittest.TestCase):
    """
    Testes automatizados para validar a calculadora de conversão de unidades do SuperCalc.
    Estes testes verificam se as conversões entre diferentes unidades estão corretas.
    """
    
    def test_conversao_comprimento(self):
        """
        Testa a conversão entre diferentes unidades de comprimento.
        """
        # Metros para centímetros
        self.assertEqual(self.converter_comprimento(1, 'm', 'cm'), 100)
        self.assertEqual(self.converter_comprimento(2.5, 'm', 'cm'), 250)
        
        # Centímetros para metros
        self.assertEqual(self.converter_comprimento(100, 'cm', 'm'), 1)
        self.assertEqual(self.converter_comprimento(250, 'cm', 'm'), 2.5)
        
        # Metros para quilômetros
        self.assertEqual(self.converter_comprimento(1000, 'm', 'km'), 1)
        self.assertEqual(self.converter_comprimento(2500, 'm', 'km'), 2.5)
        
        # Quilômetros para metros
        self.assertEqual(self.converter_comprimento(1, 'km', 'm'), 1000)
        self.assertEqual(self.converter_comprimento(2.5, 'km', 'm'), 2500)
        
        # Polegadas para centímetros
        self.assertAlmostEqual(self.converter_comprimento(1, 'in', 'cm'), 2.54, delta=0.01)
        self.assertAlmostEqual(self.converter_comprimento(10, 'in', 'cm'), 25.4, delta=0.01)
    
    def test_conversao_peso(self):
        """
        Testa a conversão entre diferentes unidades de peso/massa.
        """
        # Quilogramas para gramas
        self.assertEqual(self.converter_peso(1, 'kg', 'g'), 1000)
        self.assertEqual(self.converter_peso(2.5, 'kg', 'g'), 2500)
        
        # Gramas para quilogramas
        self.assertEqual(self.converter_peso(1000, 'g', 'kg'), 1)
        self.assertEqual(self.converter_peso(2500, 'g', 'kg'), 2.5)
        
        # Libras para quilogramas
        self.assertAlmostEqual(self.converter_peso(1, 'lb', 'kg'), 0.453592, delta=0.0001)
        self.assertAlmostEqual(self.converter_peso(10, 'lb', 'kg'), 4.53592, delta=0.0001)
        
        # Quilogramas para libras
        self.assertAlmostEqual(self.converter_peso(1, 'kg', 'lb'), 2.20462, delta=0.0001)
        self.assertAlmostEqual(self.converter_peso(5, 'kg', 'lb'), 11.0231, delta=0.0001)
    
    def test_conversao_temperatura(self):
        """
        Testa a conversão entre diferentes unidades de temperatura.
        """
        # Celsius para Fahrenheit
        self.assertAlmostEqual(self.converter_temperatura(0, 'C', 'F'), 32, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(100, 'C', 'F'), 212, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(-40, 'C', 'F'), -40, delta=0.01)
        
        # Fahrenheit para Celsius
        self.assertAlmostEqual(self.converter_temperatura(32, 'F', 'C'), 0, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(212, 'F', 'C'), 100, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(-40, 'F', 'C'), -40, delta=0.01)
        
        # Celsius para Kelvin
        self.assertAlmostEqual(self.converter_temperatura(0, 'C', 'K'), 273.15, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(100, 'C', 'K'), 373.15, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(-273.15, 'C', 'K'), 0, delta=0.01)
        
        # Kelvin para Celsius
        self.assertAlmostEqual(self.converter_temperatura(273.15, 'K', 'C'), 0, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(373.15, 'K', 'C'), 100, delta=0.01)
        self.assertAlmostEqual(self.converter_temperatura(0, 'K', 'C'), -273.15, delta=0.01)
    
    def test_conversao_volume(self):
        """
        Testa a conversão entre diferentes unidades de volume.
        """
        # Litros para mililitros
        self.assertEqual(self.converter_volume(1, 'L', 'mL'), 1000)
        self.assertEqual(self.converter_volume(2.5, 'L', 'mL'), 2500)
        
        # Mililitros para litros
        self.assertEqual(self.converter_volume(1000, 'mL', 'L'), 1)
        self.assertEqual(self.converter_volume(2500, 'mL', 'L'), 2.5)
        
        # Galões (US) para litros
        self.assertAlmostEqual(self.converter_volume(1, 'gal', 'L'), 3.78541, delta=0.0001)
        self.assertAlmostEqual(self.converter_volume(2, 'gal', 'L'), 7.57082, delta=0.0001)
        
        # Litros para galões (US)
        self.assertAlmostEqual(self.converter_volume(3.78541, 'L', 'gal'), 1, delta=0.0001)
        self.assertAlmostEqual(self.converter_volume(7.57082, 'L', 'gal'), 2, delta=0.0001)
    
    # Métodos auxiliares para realizar as conversões
    def converter_comprimento(self, valor, de, para):
        """Converte entre unidades de comprimento"""
        # Converter tudo para metros primeiro
        if de == 'cm':
            valor_m = valor / 100
        elif de == 'km':
            valor_m = valor * 1000
        elif de == 'in':
            valor_m = valor * 0.0254
        else:  # metros
            valor_m = valor
        
        # Converter de metros para a unidade desejada
        if para == 'cm':
            return valor_m * 100
        elif para == 'km':
            return valor_m / 1000
        elif para == 'in':
            return valor_m / 0.0254
        else:  # metros
            return valor_m
    
    def converter_peso(self, valor, de, para):
        """Converte entre unidades de peso/massa"""
        # Converter tudo para quilogramas primeiro
        if de == 'g':
            valor_kg = valor / 1000
        elif de == 'lb':
            valor_kg = valor * 0.453592
        else:  # quilogramas
            valor_kg = valor
        
        # Converter de quilogramas para a unidade desejada
        if para == 'g':
            return valor_kg * 1000
        elif para == 'lb':
            return valor_kg / 0.453592
        else:  # quilogramas
            return valor_kg
    
    def converter_temperatura(self, valor, de, para):
        """Converte entre unidades de temperatura"""
        # Converter tudo para Celsius primeiro
        if de == 'F':
            valor_c = (valor - 32) * 5/9
        elif de == 'K':
            valor_c = valor - 273.15
        else:  # Celsius
            valor_c = valor
        
        # Converter de Celsius para a unidade desejada
        if para == 'F':
            return valor_c * 9/5 + 32
        elif para == 'K':
            return valor_c + 273.15
        else:  # Celsius
            return valor_c
    
    def converter_volume(self, valor, de, para):
        """Converte entre unidades de volume"""
        # Converter tudo para litros primeiro
        if de == 'mL':
            valor_l = valor / 1000
        elif de == 'gal':
            valor_l = valor * 3.78541
        else:  # litros
            valor_l = valor
        
        # Converter de litros para a unidade desejada
        if para == 'mL':
            return valor_l * 1000
        elif para == 'gal':
            return valor_l / 3.78541
        else:  # litros
            return valor_l


def executar_testes_unidades():
    """
    Executa todos os testes da calculadora de unidades.
    Retorna True se todos os testes passarem, False caso contrário.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculadoraUnidades)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()


if __name__ == "__main__":
    print("\n===== TESTES DA CALCULADORA DE UNIDADES =====\n")
    sucesso = executar_testes_unidades()
    sys.exit(0 if sucesso else 1)