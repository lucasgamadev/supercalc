import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestDescontoSimplesInterface(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.url = "http://localhost:8080/pages/calc_desconto.html"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_desconto_1_a_100_porcento_valor_100(self):
        for percentual in range(1, 101):
            with self.subTest(percentual=percentual):
                self.driver.get(self.url)
                # Preencher valor
                valor_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
                valor_input.clear()
                valor_input.send_keys("100")
                # Preencher percentual
                perc_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
                perc_input.clear()
                perc_input.send_keys(str(percentual))
                # Selecionar desconto simples
                radio = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
                self.driver.execute_script("arguments[0].click();", radio)
                # Clicar calcular
                btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
                self.driver.execute_script("arguments[0].click();", btn)
                # Esperar resultado
                try:
                    self.wait.until(lambda driver: driver.find_element(By.ID, "valor-final").text != "")
                except TimeoutException:
                    self.fail(f"Timeout ao calcular desconto para percentual {percentual}")
                # Validar resultado
                valor_final = self.driver.find_element(By.ID, "valor-final").text
                valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
                # Converter para float
                try:
                    valor_final_num = float(valor_final.replace(".", "").replace(",", "."))
                    valor_desconto_num = float(valor_desconto.replace(".", "").replace(",", "."))
                except ValueError:
                    self.fail(f"Conversão inválida para percentual {percentual}")
                esperado_desconto = 100 * percentual / 100
                esperado_final = 100 - esperado_desconto
                self.assertAlmostEqual(valor_desconto_num, esperado_desconto, delta=0.01, msg=f"Desconto errado para {percentual}%")
                self.assertAlmostEqual(valor_final_num, esperado_final, delta=0.01, msg=f"Valor final errado para {percentual}%")

if __name__ == "__main__":
    unittest.main()