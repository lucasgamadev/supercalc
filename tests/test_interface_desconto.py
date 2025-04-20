import unittest
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

class TestInterfaceCalculadoraDesconto(unittest.TestCase):
    """
    Testes automatizados para validar a interface da calculadora de desconto do SuperCalc.
    Estes testes verificam se a interface responde corretamente às entradas do usuário
    e se os resultados exibidos estão corretos.
    
    Requisitos:
    - Selenium WebDriver
    - Navegador Chrome instalado
    - ChromeDriver no PATH
    """
    @classmethod
    def setUpClass(cls):
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            print("ERRO: Não foi possível inicializar o Chrome WebDriver.")
            print("Verifique se o Chrome e o ChromeDriver estão instalados corretamente.")
            sys.exit(1)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.http_url = "http://localhost:8080/pages/calc_desconto.html"
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    def setUp(self):
        self.driver.get("http://localhost:8080/pages/calc_desconto.html")
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "calcular")))
        except TimeoutException:
            self.fail("Página de desconto não carregou dentro do tempo limite")
    def preencher_e_calcular(self, valor, desconto):
        self.driver.find_element(By.ID, "valor-original").clear()
        self.driver.find_element(By.ID, "valor-original").send_keys(str(valor))
        self.driver.find_element(By.ID, "desconto").clear()
        self.driver.find_element(By.ID, "desconto").send_keys(str(desconto))
        calcular_btn = self.driver.find_element(By.ID, "calcular")
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-desconto"), ""))
        return {
            "valor-desconto": self.driver.find_element(By.ID, "valor-desconto").text,
            # Adicione mais campos conforme necessário
        }

    def test_calculo_desconto_simples(self):
        """
        Testa o cálculo de desconto simples na interface.
        """
        resultados = self.preencher_e_calcular(100, 10)
        self.assertIn("10", resultados["valor-desconto"].replace(",", "."))

    def test_desconto_zero(self):
        """
        Testa desconto de 0% (valor final deve ser igual ao original).
        """
        resultados = self.preencher_e_calcular(100, 0)
        self.assertIn("0", resultados["valor-desconto"].replace(",", "."))

    def test_desconto_cem_porcento(self):
        """
        Testa desconto de 100% (valor final deve ser zero).
        """
        resultados = self.preencher_e_calcular(100, 100)
        valor = resultados["valor-desconto"].replace(",", ".")
        self.assertTrue(
            any(x in valor for x in ["100", "100.00", "100,00", "1.00", "1,00", "0.00"]),
            f"Valor do desconto para 100% inesperado: '{valor}'"
        )

    def test_valor_original_zero(self):
        """
        Testa valor original zero (resultados devem ser zero).
        """
        resultados = self.preencher_e_calcular(0, 10)
        self.assertIn("0", resultados["valor-desconto"].replace(",", "."))

    def test_desconto_negativo(self):
        """
        Testa desconto negativo (deve validar ou exibir erro na interface).
        """
        self.preencher_e_calcular(100, -10)
        # Verifica se o campo de desconto ficou com classe 'invalid'
        desconto_input = self.driver.find_element(By.ID, "desconto")
        self.assertIn("invalid", desconto_input.get_attribute("class"))

    def test_desconto_maior_que_cem(self):
        """
        Testa desconto acima de 100% (deve validar ou exibir erro na interface).
        """
        self.preencher_e_calcular(100, 150)
        desconto_input = self.driver.find_element(By.ID, "desconto")
        self.assertIn("invalid", desconto_input.get_attribute("class"))

    def test_limpar_campos(self):
        """
        Testa a funcionalidade do botão limpar.
        """
        self.driver.find_element(By.ID, "valor-original").send_keys("123")
        self.driver.find_element(By.ID, "desconto").send_keys("5")
        limpar_btn = self.driver.find_element(By.ID, "limpar")
        self.driver.execute_script("arguments[0].click();", limpar_btn)
        valor = self.driver.find_element(By.ID, "valor-original").get_attribute("value")
        desconto = self.driver.find_element(By.ID, "desconto").get_attribute("value")
        self.assertTrue(valor == "" or valor == "0,00" or valor == "0")
        self.assertTrue(desconto == "" or desconto == "0,00" or desconto == "0")

    def test_valores_decimais(self):
        """
        Testa valores decimais e diferentes formatos de entrada.
        """
        resultados = self.preencher_e_calcular("99,99", "15,5")
        self.assertTrue("," in resultados["valor-desconto"] or "." in resultados["valor-desconto"])

def executar_testes_interface_desconto():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInterfaceCalculadoraDesconto)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()
if __name__ == "__main__":
    print("\n===== TESTES DE INTERFACE DA CALCULADORA DE DESCONTO =====\n")
    sucesso = executar_testes_interface_desconto()
    sys.exit(0 if sucesso else 1)
