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
    def test_calculo_desconto_simples(self):
        """
        Testa o cálculo de desconto simples na interface.
        """
        # Preencher os campos
        self.driver.find_element(By.ID, "valor-original").clear()
        self.driver.find_element(By.ID, "valor-original").send_keys("100")
        self.driver.find_element(By.ID, "desconto").clear()
        self.driver.find_element(By.ID, "desconto").send_keys("10")
        # Clicar no botão calcular
        calcular_btn = self.driver.find_element(By.ID, "calcular")
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        # Esperar resultado
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-desconto"), ""))
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        preco_final = self.driver.find_element(By.ID, "preco-final").text
        # Verifica se o desconto e valor final estão corretos (100 - 10%)
        self.assertTrue("10" in valor_desconto.replace(",", "."), f"Valor do desconto incorreto: {valor_desconto}")
        self.assertTrue("90" in preco_final.replace(",", "."), f"Preço final incorreto: {preco_final}")
def executar_testes_interface_desconto():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInterfaceCalculadoraDesconto)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()
if __name__ == "__main__":
    print("\n===== TESTES DE INTERFACE DA CALCULADORA DE DESCONTO =====\n")
    sucesso = executar_testes_interface_desconto()
    sys.exit(0 if sucesso else 1)
