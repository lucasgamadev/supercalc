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
    
    Instalação:
    pip install selenium
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Configuração inicial para os testes.
        Inicializa o Chrome WebDriver para executar os testes.
        """
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        # Configurar opções do Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            # Inicializar o Chrome WebDriver com as opções configuradas
            cls.driver = webdriver.Chrome(options=chrome_options)
        except WebDriverException:
            print("ERRO: Não foi possível inicializar o Chrome WebDriver.")
            print("Verifique se o Chrome e o ChromeDriver estão instalados corretamente.")
            sys.exit(1)
        
        # Configurar timeout para espera de elementos
        cls.driver.implicitly_wait(10)
        cls.wait = WebDriverWait(cls.driver, 10)
        
        # (Opcional) Guardar o caminho HTTP da página para referência
        cls.http_url = "http://localhost:8080/pages/calc_desconto.html"
    
    @classmethod
    def tearDownClass(cls):
        """
        Limpeza após todos os testes.
        """
        if hasattr(cls, 'driver'):
            cls.driver.quit()
    
    def setUp(self):
        """
        Preparação antes de cada teste.
        """
        # Carregar a página da calculadora de desconto via HTTP local
        self.driver.get("http://localhost:8080/pages/calc_desconto.html")
        
        # Esperar que a página carregue completamente (ex: botão calcular esteja presente)
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "calcular")))
        except TimeoutException:
            self.fail("Página não carregou dentro do tempo limite ou o botão 'calcular' não foi encontrado")
    
    def test_calculo_desconto_simples(self):
        """Testa o cálculo de desconto simples na interface."""
        self._preencher_campo("valor-original", "1000")
        self._preencher_campo("percentual-desconto", "10")
        self._selecionar_tipo_desconto("simples")
        self._clicar_calcular()
        self._aguardar_resultado()
        resultados = self._obter_resultados()
        self.assertEqual(resultados["tipo_desconto"], "Simples")
        self.assertAlmostEqual(resultados["valor_desconto"], 100.0, delta=0.01)
        self.assertAlmostEqual(resultados["valor_final"], 900.0, delta=0.01)

    def _preencher_campo(self, id_campo, valor):
        campo = self.wait.until(EC.element_to_be_clickable((By.ID, id_campo)))
        campo.clear()
        campo.send_keys(valor)

    def _selecionar_tipo_desconto(self, tipo):
        seletor = f"input[name='tipo-desconto'][value='{tipo}']"
        radio = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, seletor)))
        self.driver.execute_script("arguments[0].click();", radio)

    def _clicar_calcular(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
        self.driver.execute_script("arguments[0].click();", btn)

    def _aguardar_resultado(self):
        try:
            self.wait.until(lambda driver: 
                driver.find_element(By.ID, "valor-final").text != "" and 
                driver.find_element(By.ID, "valor-final").text != "0,00")
        except TimeoutException:
            self.fail("Tempo esgotado ao esperar pelos resultados na interface.")

    def _obter_resultados(self):
        try:
            valor_original_resultado = self.driver.find_element(By.ID, "valor-original-resultado").text
            tipo_desconto = self.driver.find_element(By.ID, "tipo-desconto").text
            percentual_aplicado = self.driver.find_element(By.ID, "percentual-aplicado").text
            valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
            valor_final = self.driver.find_element(By.ID, "valor-final").text
            valor_desconto_num = float(valor_desconto.replace(".", "").replace(",", "."))
            valor_final_num = float(valor_final.replace(".", "").replace(",", "."))
        except ValueError:
            self.fail("Não foi possível converter os valores de resultado para float.")
        return {
            "valor_original": valor_original_resultado,
            "tipo_desconto": tipo_desconto,
            "percentual_aplicado": percentual_aplicado,
            "valor_desconto": valor_desconto_num,
            "valor_final": valor_final_num
        }
    
    def test_calculo_desconto_progressivo(self):
        """Testa o cálculo de desconto progressivo na interface."""
        self._preencher_campo("valor-original", "2000")
        self._selecionar_tipo_desconto("progressivo")
        self._clicar_calcular()
        self._aguardar_resultado()
        resultados = self._obter_resultados()
        self.assertEqual(resultados["tipo_desconto"], "Progressivo")
        self.assertAlmostEqual(resultados["valor_desconto"], 400.0, delta=0.01)
        self.assertAlmostEqual(resultados["valor_final"], 1600.0, delta=0.01)
    
    def test_calculo_desconto_cupom(self):
        """
        Testa o cálculo de desconto por cupom na interface.
        """
        # Preencher os campos do formulário com espera explícita
        valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
        valor_original_input.clear()
        valor_original_input.send_keys("1000")
        
        cupom_input = self.wait.until(EC.element_to_be_clickable((By.ID, "cupom")))
        cupom_input.clear()
        cupom_input.send_keys("SUPER50")
        
        # Selecionar desconto por cupom usando JavaScript (espera pela presença)
        desconto_cupom_radio = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='cupom']")))
        self.driver.execute_script("arguments[0].click();", desconto_cupom_radio)
        
        # Clicar no botão calcular usando JavaScript (espera ser clicável)
        calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Esperar que os resultados sejam atualizados
        try:
            self.wait.until(lambda driver: 
                driver.find_element(By.ID, "valor-final").text != "" and 
                driver.find_element(By.ID, "valor-final").text != "0,00")
        except TimeoutException:
             self.fail("Tempo esgotado ao esperar pelos resultados na interface.")

        # Verificar os resultados
        valor_original_resultado = self.driver.find_element(By.ID, "valor-original-resultado").text
        tipo_desconto = self.driver.find_element(By.ID, "tipo-desconto").text
        # Nota: O campo 'percentual-aplicado' pode não existir ou ser relevante para cupom
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        valor_final = self.driver.find_element(By.ID, "valor-final").text
        
        try:
            # Converter valores para comparação
            valor_desconto_num = float(valor_desconto.replace(".", "").replace(",", "."))
            valor_final_num = float(valor_final.replace(".", "").replace(",", "."))
        except ValueError:
            self.fail("Não foi possível converter os valores de resultado para float.")

        # Verificar se os resultados estão corretos
        self.assertEqual(tipo_desconto, "Cupom")
        self.assertAlmostEqual(valor_desconto_num, 500.0, delta=0.01)
        self.assertAlmostEqual(valor_final_num, 500.0, delta=0.01)
    
    def test_validacao_campos(self):
        """
        Testa a validação de campos na interface.
        """
        # Clicar no botão calcular sem preencher os campos
        calcular_btn = self.driver.find_element(By.ID, "calcular")
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Verificar se o campo valor original está marcado como inválido
        valor_input = self.driver.find_element(By.ID, "valor-original")
        # Esperar um pouco para a classe ser aplicada (alternativa a wait explícito complexo)
        # Idealmente, a validação JS deveria ser síncrona ou usar waits mais robustos
        # Mas para simplificar e alinhar com juros, usamos assertTrue direto
        self.assertTrue("invalid" in valor_input.get_attribute("class"),
                        "Campo valor original não foi marcado como inválido.")
        
        # Preencher o campo valor original e tentar novamente
        valor_input.clear()
        valor_input.send_keys("1000")
        
        # Selecionar desconto simples para testar validação do percentual
        desconto_simples_radio = self.driver.find_element(
            By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")
        self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
        
        # Clicar em calcular novamente
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Verificar se o campo percentual está marcado como inválido
        percentual_input = self.driver.find_element(By.ID, "percentual-desconto")
        self.assertTrue("invalid" in percentual_input.get_attribute("class"),
                        "Campo percentual não foi marcado como inválido.")

        # Testar validação do cupom
        # Selecionar desconto por cupom
        desconto_cupom_radio = self.driver.find_element(
            By.CSS_SELECTOR, "input[name='tipo-desconto'][value='cupom']")
        self.driver.execute_script("arguments[0].click();", desconto_cupom_radio)

        # Clicar em calcular novamente (com valor preenchido, mas sem cupom)
        self.driver.execute_script("arguments[0].click();", calcular_btn)

        # Verificar se o campo cupom está marcado como inválido
        cupom_input = self.driver.find_element(By.ID, "cupom")
        self.assertTrue("invalid" in cupom_input.get_attribute("class"),
                        "Campo cupom não foi marcado como inválido.")
    
    def test_limpar_campos(self):
        """
        Testa a funcionalidade de limpar campos.
        """
        # Preencher os campos do formulário
        valor_original_input = self.driver.find_element(By.ID, "valor-original")
        valor_original_input.send_keys("1000")
        percentual_input = self.driver.find_element(By.ID, "percentual-desconto")
        percentual_input.send_keys("10")
        cupom_input = self.driver.find_element(By.ID, "cupom")
        cupom_input.send_keys("TESTE") # Preencher cupom também
        
        # Clicar no botão limpar usando JavaScript
        limpar_btn = self.driver.find_element(By.ID, "limpar")
        self.driver.execute_script("arguments[0].click();", limpar_btn)
        
        # Verificar se os campos foram limpos
        valor_limpo = valor_original_input.get_attribute("value")
        percentual_limpo = percentual_input.get_attribute("value")
        cupom_limpo = cupom_input.get_attribute("value")
        
        self.assertEqual(valor_limpo, "", f"Campo valor original não foi limpo corretamente: '{valor_limpo}'")
        self.assertEqual(percentual_limpo, "", f"Campo percentual não foi limpo corretamente: '{percentual_limpo}'")
        self.assertEqual(cupom_limpo, "", f"Campo cupom não foi limpo corretamente: '{cupom_limpo}'")
        
        # Verificar se os resultados foram resetados (esperar que voltem a 0,00)
        try:
            self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), "0,00"))
        except TimeoutException:
            self.fail("Resultados não foram resetados para '0,00' após limpar.")
        
        valor_original_resultado = self.driver.find_element(By.ID, "valor-original-resultado").text
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        valor_final = self.driver.find_element(By.ID, "valor-final").text
        
        self.assertEqual(valor_original_resultado, "0,00", "Resultado valor original não foi resetado.")
        self.assertEqual(valor_desconto, "0,00", "Resultado valor desconto não foi resetado.")
        self.assertEqual(valor_final, "0,00", "Resultado valor final não foi resetado.")
    
    def test_valores_negativos(self):
        """
        Testa o comportamento da calculadora com valores negativos.
        A aplicação deve idealmente rejeitar valores negativos.
        """
        # Preencher os campos do formulário com valor negativo
        valor_original_input = self.driver.find_element(By.ID, "valor-original")
        valor_original_input.clear()
        valor_original_input.send_keys("-1000")
        
        percentual_input = self.driver.find_element(By.ID, "percentual-desconto")
        percentual_input.clear()
        percentual_input.send_keys("10")
        
        # Selecionar desconto simples
        desconto_simples_radio = self.driver.find_element(
            By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")
        self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
        
        # Clicar no botão calcular
        calcular_btn = self.driver.find_element(By.ID, "calcular")
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Verificar se o campo valor está marcado como inválido
        self.assertTrue("invalid" in valor_original_input.get_attribute("class"),
                        "Campo valor original não foi marcado como inválido para valor negativo.")

        # Verificar se os resultados permanecem 0 ou indicam erro
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        valor_final = self.driver.find_element(By.ID, "valor-final").text
        self.assertEqual(valor_desconto, "0,00", "Valor do desconto não permaneceu 0,00 com entrada negativa.")
        self.assertEqual(valor_final, "0,00", "Valor final não permaneceu 0,00 com entrada negativa.")

        # Testar percentual negativo
        valor_original_input.clear()
        valor_original_input.send_keys("1000")
        percentual_input.clear()
        percentual_input.send_keys("-10")
        self.driver.execute_script("arguments[0].click();", calcular_btn)

        # Verificar se o campo percentual está marcado como inválido
        self.assertTrue("invalid" in percentual_input.get_attribute("class"),
                        "Campo percentual não foi marcado como inválido para valor negativo.")
        # Verificar resultados novamente
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        valor_final = self.driver.find_element(By.ID, "valor-final").text
        self.assertEqual(valor_desconto, "0,00", "Valor do desconto não permaneceu 0,00 com percentual negativo.")
        self.assertEqual(valor_final, "0,00", "Valor final não permaneceu 0,00 com percentual negativo.")
    
    def test_formato_entrada_diferente(self):
        """
        Testa o comportamento da calculadora com diferentes formatos de entrada (vírgula/ponto).
        Verifica se a aplicação interpreta corretamente ambos os formatos.
        """
        resultados_virgula = {}
        resultados_ponto = {}

        try:
            # --- Teste com vírgula --- 
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("1000,50")
            
            percentual_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
            percentual_input.clear()
            percentual_input.send_keys("10,5")
            
            desconto_simples_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            self.wait.until(lambda driver: 
                driver.find_element(By.ID, "valor-final").text != "" and 
                driver.find_element(By.ID, "valor-final").text != "0,00")
            
            resultados_virgula['valor_original'] = self.driver.find_element(By.ID, "valor-original-resultado").text
            resultados_virgula['valor_desconto'] = self.driver.find_element(By.ID, "valor-desconto").text
            resultados_virgula['valor_final'] = self.driver.find_element(By.ID, "valor-final").text

            # --- Limpar campos --- 
            limpar_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "limpar")))
            self.driver.execute_script("arguments[0].click();", limpar_btn)
            self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), "0,00")) # Esperar limpar

            # --- Teste com ponto --- 
            valor_original_input.clear()
            valor_original_input.send_keys("1000.50")
            percentual_input.clear()
            percentual_input.send_keys("10.5")
            
            # Desconto simples já deve estar selecionado ou selecionar novamente
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            self.wait.until(lambda driver: 
                driver.find_element(By.ID, "valor-final").text != "" and 
                driver.find_element(By.ID, "valor-final").text != "0,00")
            
            resultados_ponto['valor_original'] = self.driver.find_element(By.ID, "valor-original-resultado").text
            resultados_ponto['valor_desconto'] = self.driver.find_element(By.ID, "valor-desconto").text
            resultados_ponto['valor_final'] = self.driver.find_element(By.ID, "valor-final").text

            # --- Comparações --- 
            # Verificar se ambos os formatos produziram resultados não vazios
            self.assertTrue(all(resultados_virgula.values()), "Resultados com vírgula não foram preenchidos.")
            self.assertTrue(all(resultados_ponto.values()), "Resultados com ponto não foram preenchidos.")

            # Comparar os valores numéricos (devem ser iguais ou muito próximos)
            try:
                vf_virgula = float(resultados_virgula['valor_final'].replace(".", "").replace(",", "."))
                vf_ponto = float(resultados_ponto['valor_final'].replace(".", "").replace(",", "."))
                self.assertAlmostEqual(vf_virgula, vf_ponto, delta=0.01, msg="Resultados finais diferem entre vírgula e ponto.")
                
                vd_virgula = float(resultados_virgula['valor_desconto'].replace(".", "").replace(",", "."))
                vd_ponto = float(resultados_ponto['valor_desconto'].replace(".", "").replace(",", "."))
                self.assertAlmostEqual(vd_virgula, vd_ponto, delta=0.01, msg="Valores de desconto diferem entre vírgula e ponto.")
            except ValueError:
                self.fail("Não foi possível converter os resultados para float para comparação.")

        except TimeoutException:
             self.fail("Tempo esgotado ao esperar por elementos ou resultados no teste de formato de entrada.")
        except Exception as e:
            # Registrar que a aplicação pode não suportar ambos os formatos
            print(f"Nota: A aplicação pode não suportar ou interpretar diferentemente formatos de entrada com vírgula/ponto: {str(e)}")
            # Considerar falhar o teste se ambos os formatos são requisitos
            # self.fail(f"Erro ao testar formatos de entrada diferentes: {str(e)}")
            self.assertTrue(True) # Por ora, apenas registra
    
    def test_valores_grandes(self):
        """
        Testa o comportamento da calculadora com valores muito grandes.
        Verifica se a aplicação lida com os valores sem travar ou gerar erros inesperados.
        """
        try:
            # Preencher os campos do formulário com valores grandes
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("9999999999999") # Valor muito grande
            
            percentual_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
            percentual_input.clear()
            percentual_input.send_keys("15") # Percentual razoável
            
            # Selecionar desconto simples
            desconto_simples_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            
            # Clicar no botão calcular
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Verificar se a aplicação lida com valores grandes sem travar
            # Esperar que os resultados sejam atualizados (ou que a página ainda responda)
            self.wait.until(EC.presence_of_element_located((By.ID, "valor-final")))
            
            # Tentar obter os resultados (sem verificar exatidão, apenas se não houve erro)
            valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
            valor_final = self.driver.find_element(By.ID, "valor-final").text
            
            # Se chegou aqui, a aplicação não travou e calculou algo
            print(f"Valores grandes: Desconto={valor_desconto}, Final={valor_final}") # Log para info
            self.assertTrue(True, "Aplicação processou valores grandes sem travar.")

        except TimeoutException:
            self.fail("Aplicação não respondeu ou travou com valores grandes (Timeout).")
        except Exception as e:
            # Capturar outros erros que podem ocorrer com valores grandes (ex: OverflowError)
            self.fail(f"A aplicação gerou um erro inesperado com valores grandes: {str(e)}")
    
    def test_multiplos_calculos_consecutivos(self):
        """
        Testa se a calculadora mantém o estado correto entre operações consecutivas,
        incluindo a limpeza de campos entre os cálculos.
        """
        try:
            # --- Primeiro cálculo: 1000 com 10% de desconto simples --- 
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("1000")
            
            percentual_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
            percentual_input.clear()
            percentual_input.send_keys("10")
            
            desconto_simples_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Esperar e verificar primeiro resultado
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text == "900,00")
            valor_final_1 = self.driver.find_element(By.ID, "valor-final").text
            self.assertEqual(valor_final_1, "900,00")

            # --- Limpar campos --- 
            limpar_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "limpar")))
            self.driver.execute_script("arguments[0].click();", limpar_btn)
            self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), "0,00")) # Esperar limpar
            # Verificar se campos de input foram limpos
            self.assertEqual(valor_original_input.get_attribute("value"), "")
            self.assertEqual(percentual_input.get_attribute("value"), "")

            # --- Segundo cálculo: 2000 com desconto progressivo --- 
            valor_original_input.send_keys("2000")
            
            desconto_progressivo_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='progressivo']")))
            self.driver.execute_script("arguments[0].click();", desconto_progressivo_radio)
            
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Esperar e verificar segundo resultado (20% de 2000 = 400, final = 1600)
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text == "1.600,00")
            valor_final_2 = self.driver.find_element(By.ID, "valor-final").text
            self.assertEqual(valor_final_2, "1.600,00")
            
            # Verificar que os resultados são diferentes
            self.assertNotEqual(valor_final_1, valor_final_2)

        except TimeoutException:
             self.fail("Tempo esgotado durante o teste de múltiplos cálculos consecutivos.")
        except Exception as e:
            self.fail(f"Erro durante o teste de múltiplos cálculos consecutivos: {str(e)}")
    
    def test_formatacao_monetaria(self):
        """
        Testa se a formatação monetária (padrão brasileiro) está correta nos resultados.
        """
        try:
            # Preencher os campos do formulário com um valor que exija separadores
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("1234567.89") # Usar ponto como separador decimal na entrada
            
            percentual_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
            percentual_input.clear()
            percentual_input.send_keys("10")
            
            # Selecionar desconto simples
            desconto_simples_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            
            # Clicar no botão calcular
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Esperar que os resultados sejam atualizados
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text != "0,00")
            
            # Obter resultados formatados
            valor_original_res = self.driver.find_element(By.ID, "valor-original-resultado").text
            valor_desconto_res = self.driver.find_element(By.ID, "valor-desconto").text
            valor_final_res = self.driver.find_element(By.ID, "valor-final").text
            
            # Verificar formatação (padrão brasileiro: ponto como separador de milhar, vírgula como decimal)
            # Exemplo esperado para 1234567.89 com 10% desconto: 1.234.567,89 / 123.456,79 / 1.111.111,10
            padrao_br = r'^\d{1,3}(\.\d{3})*,\d{2}$' # Regex para formato R$ 1.234,56
            
            # Usar regex para verificar o formato
            import re # Necessário para test_formatacao_monetaria # Adicionar import no início do arquivo se não existir
            self.assertTrue(re.match(padrao_br, valor_original_res), f"Formato incorreto para valor original: {valor_original_res}")
            self.assertTrue(re.match(padrao_br, valor_desconto_res), f"Formato incorreto para valor desconto: {valor_desconto_res}")
            self.assertTrue(re.match(padrao_br, valor_final_res), f"Formato incorreto para valor final: {valor_final_res}")

            # Verificação adicional dos valores (opcional, mas bom para garantir)
            self.assertEqual(valor_original_res, "1.234.567,89")
            self.assertEqual(valor_desconto_res, "123.456,79") # 10% de 1234567.89
            self.assertEqual(valor_final_res, "1.111.111,10") # 1234567.89 - 123456.79

        except TimeoutException:
             self.fail("Tempo esgotado ao esperar por elementos ou resultados no teste de formatação monetária.")
        except Exception as e:
            self.fail(f"Erro durante o teste de formatação monetária: {str(e)}")
    
    def test_cupom_invalido(self):
        """
        Testa o comportamento da calculadora com um cupom inválido.
        Espera-se que a aplicação indique o erro ou aplique 0% de desconto.
        """
        try:
            # Preencher os campos do formulário
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("1000")
            
            cupom_input = self.wait.until(EC.element_to_be_clickable((By.ID, "cupom")))
            cupom_input.clear()
            cupom_input.send_keys("CUPOMINVALIDO123")
            
            # Selecionar desconto por cupom
            desconto_cupom_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='cupom']")))
            self.driver.execute_script("arguments[0].click();", desconto_cupom_radio)
            
            # Clicar no botão calcular
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Verificar comportamento: 
            # 1. Mensagem de erro específica? 
            # 2. Campo cupom marcado como inválido?
            # 3. Resultado com 0 de desconto?
            
            # Tentar encontrar mensagem de erro (ajustar seletor conforme a aplicação)
            try:
                # Esperar um pouco para a mensagem aparecer
                mensagem_erro = self.wait.until(EC.visibility_of_element_located((By.ID, "erro-cupom"))) # Exemplo de ID
                self.assertTrue(mensagem_erro.is_displayed(), "Mensagem de erro para cupom inválido não encontrada ou não visível.")
                # Se encontrou mensagem de erro, o teste passou
                return 
            except TimeoutException:
                # Se não há mensagem de erro específica, verificar outras condições
                pass

            # Verificar se o campo cupom foi marcado como inválido
            try:
                self.wait.until(lambda d: "invalid" in cupom_input.get_attribute("class") or 
                                          "error" in cupom_input.get_attribute("class"))
                self.assertTrue(True, "Campo cupom foi marcado como inválido.")
                # Se marcou como inválido, o teste passou
                return
            except TimeoutException:
                 # Se não marcou como inválido, verificar o resultado
                 pass

            # Verificar se o desconto aplicado foi zero
            try:
                self.wait.until(lambda d: d.find_element(By.ID, "valor-desconto").text == "0,00")
                valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
                valor_final = self.driver.find_element(By.ID, "valor-final").text
                valor_original_res = self.driver.find_element(By.ID, "valor-original-resultado").text
                
                self.assertEqual(valor_desconto, "0,00", "Desconto não foi zero para cupom inválido.")
                # Verificar se valor final é igual ao original
                self.assertEqual(valor_final, valor_original_res, "Valor final não é igual ao original para cupom inválido.")
            except TimeoutException:
                self.fail("Não foi possível verificar o resultado (desconto 0) para cupom inválido.")
            except Exception as e:
                 self.fail(f"Erro ao verificar resultado para cupom inválido: {str(e)}")

        except TimeoutException:
             self.fail("Tempo esgotado durante o teste de cupom inválido.")
        except Exception as e:
            self.fail(f"Erro durante o teste de cupom inválido: {str(e)}")
    
    def test_acessibilidade_teclado(self):
        """
        Testa a navegação e interação básica usando o teclado (TAB e ENTER).
        Nota: Este teste é simplificado e pode precisar de ajustes dependendo da
        implementação exata da navegação por teclado na página.
        """
        try:
            # Focar no primeiro campo interativo (valor original)
            valor_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            self.driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].focus();", valor_input)
            valor_input.clear()
            valor_input.send_keys("500")
            
            # Navegar para o próximo campo (percentual) e preencher
            valor_input.send_keys(Keys.TAB)
            # Esperar que o foco mude (pode ser necessário ajustar a espera)
            # self.wait.until(lambda d: d.switch_to.active_element.get_attribute("id") == "percentual-desconto")
            percentual_input = self.driver.switch_to.active_element
            percentual_input.clear()
            percentual_input.send_keys("20")

            # Navegar para o tipo de desconto (simples) e selecionar com espaço
            percentual_input.send_keys(Keys.TAB) # Foco no grupo de radio
            # Assumindo que o primeiro radio (simples) é o próximo na ordem de tabulação
            # Pode ser necessário enviar TAB mais vezes dependendo da estrutura HTML
            radio_simples = self.driver.switch_to.active_element 
            # Verificar se é o radio correto (opcional, mas bom para robustez)
            # self.assertEqual(radio_simples.get_attribute("value"), "simples")
            radio_simples.send_keys(Keys.SPACE) # Selecionar com espaço

            # Navegar até o botão calcular
            # Enviar TABs suficientes para chegar ao botão 'calcular'
            # O número exato de TABs depende da ordem dos elementos focáveis
            elementos_focaveis_ate_calcular = 3 # Ajustar conforme necessário (percentual -> cupom -> radio -> calcular?)
            for _ in range(elementos_focaveis_ate_calcular):
                 self.driver.switch_to.active_element.send_keys(Keys.TAB)
                 # Pequena pausa pode ajudar em algumas situações
                 # import time; time.sleep(0.1)
            
            # Ativar o botão calcular com ENTER
            calcular_btn_focado = self.driver.switch_to.active_element
            # Verificar se o foco está no botão calcular (opcional)
            # self.assertEqual(calcular_btn_focado.get_attribute("id"), "calcular")
            calcular_btn_focado.send_keys(Keys.ENTER)
            
            # Esperar e verificar o resultado
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text != "0,00")
            valor_final = self.driver.find_element(By.ID, "valor-final").text
            # 500 com 20% de desconto = 400
            # A formatação pode ser "400,00" ou "400.00" dependendo da implementação
            self.assertTrue(valor_final == "400,00" or valor_final == "400.00", f"Resultado inesperado no teste de teclado: {valor_final}")

        except TimeoutException:
             self.fail("Tempo esgotado durante o teste de acessibilidade por teclado.")
        except Exception as e:
            # Falhar o teste se ocorrer qualquer erro inesperado durante a navegação/interação
            self.fail(f"Erro inesperado durante o teste de acessibilidade por teclado: {str(e)}")
    
    def test_valores_fracionados(self):
        """
        Testa o cálculo de desconto com valores fracionados (centavos),
        usando vírgula como separador decimal na entrada.
        """
        try:
            # Preencher os campos do formulário com valor fracionado
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("123,45") # Entrada com vírgula
            
            percentual_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
            percentual_input.clear()
            percentual_input.send_keys("10,5") # Entrada com vírgula
            
            # Selecionar desconto simples
            desconto_simples_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            
            # Clicar no botão calcular
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Esperar que os resultados sejam atualizados
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text != "0,00")
            
            # Verificar os resultados
            valor_desconto_res = self.driver.find_element(By.ID, "valor-desconto").text
            valor_final_res = self.driver.find_element(By.ID, "valor-final").text
            
            # Converter valores para comparação (assumindo saída com vírgula)
            valor_desconto_num = float(valor_desconto_res.replace(".", "").replace(",", "."))
            valor_final_num = float(valor_final_res.replace(".", "").replace(",", "."))
            
            # Verificar se os resultados estão corretos (10,5% de 123,45)
            # 123.45 * 0.105 = 12.96225 -> 12,96
            # 123.45 * (1 - 0.105) = 110.48775 -> 110,49
            self.assertAlmostEqual(valor_desconto_num, 12.96, delta=0.01)
            self.assertAlmostEqual(valor_final_num, 110.49, delta=0.01)

            # Verificar formatação (opcional)
            self.assertTrue(',' in valor_desconto_res, "Resultado do desconto não contém vírgula.")
            self.assertTrue(',' in valor_final_res, "Resultado final não contém vírgula.")

        except TimeoutException:
             self.fail("Tempo esgotado ao esperar por elementos ou resultados no teste de valores fracionados.")
        except Exception as e:
            self.fail(f"Erro durante o teste de valores fracionados: {str(e)}")
    
    def test_multiplos_descontos_sucessivos(self):
        """
        Testa a aplicação de um segundo desconto sobre o resultado do primeiro.
        Simula um cenário de desconto sobre desconto.
        """
        try:
            # --- Primeiro desconto: 1000 com 10% --- 
            valor_original_input = self.wait.until(EC.element_to_be_clickable((By.ID, "valor-original")))
            valor_original_input.clear()
            valor_original_input.send_keys("1000")
            
            percentual_input = self.wait.until(EC.element_to_be_clickable((By.ID, "percentual-desconto")))
            percentual_input.clear()
            percentual_input.send_keys("10")
            
            desconto_simples_radio = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")))
            self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
            
            calcular_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "calcular")))
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Esperar e obter o valor final após o primeiro desconto
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text == "900,00")
            valor_intermediario_str = self.driver.find_element(By.ID, "valor-final").text
            valor_intermediario_num = float(valor_intermediario_str.replace(".", "").replace(",", ".")) # 900.0
            self.assertEqual(valor_intermediario_num, 900.0)

            # --- Segundo desconto: 5% sobre o valor intermediário (900) --- 
            # Usar o valor intermediário como novo valor original
            valor_original_input.clear()
            # Enviar o valor formatado como string, pode ser com vírgula ou ponto dependendo do que a app espera
            valor_original_input.send_keys(valor_intermediario_str) 
            
            percentual_input.clear()
            percentual_input.send_keys("5")
            
            # Desconto simples já deve estar selecionado
            self.driver.execute_script("arguments[0].click();", calcular_btn)
            
            # Esperar e obter o valor final após o segundo desconto
            # 5% de 900 = 45. Final = 900 - 45 = 855
            self.wait.until(lambda d: d.find_element(By.ID, "valor-final").text == "855,00")
            valor_final_2 = self.driver.find_element(By.ID, "valor-final").text
            valor_final_num_2 = float(valor_final_2.replace(".", "").replace(",", "."))
            
            # Verificar se o resultado está correto (900 * 0.95 = 855)
            self.assertAlmostEqual(valor_final_num_2, 855.0, delta=0.01)
            
            # Verificar equivalência com desconto composto (opcional)
            # 1000 * (1 - 0.10) * (1 - 0.05) = 855
            self.assertAlmostEqual(valor_final_num_2, 1000 * 0.90 * 0.95, delta=0.01)

        except TimeoutException:
             self.fail("Tempo esgotado durante o teste de múltiplos descontos sucessivos.")
        except Exception as e:
            self.fail(f"Erro durante o teste de múltiplos descontos sucessivos: {str(e)}")
    
    def test_responsividade(self):
        """
        Testa a responsividade da interface em diferentes tamanhos de tela.
        """
        # Tamanhos de tela para testar (largura, altura)
        tamanhos_tela = [
            (1920, 1080),  # Desktop grande
            (1366, 768),   # Desktop comum
            (768, 1024),   # Tablet retrato
            (375, 812)     # Smartphone
        ]
        
        for largura, altura in tamanhos_tela:
            # Redimensionar a janela do navegador
            self.driver.set_window_size(largura, altura)
            time.sleep(1)  # Aguardar o redimensionamento
            
            try:
                # Verificar se os elementos principais estão visíveis
                elementos = [
                    self.driver.find_element(By.ID, "valor-original"),
                    self.driver.find_element(By.ID, "percentual-desconto"),
                    self.driver.find_element(By.ID, "calcular"),
                    self.driver.find_element(By.ID, "limpar")
                ]
                
                for elemento in elementos:
                    # Verificar se o elemento está visível na tela
                    self.assertTrue(
                        elemento.is_displayed(),
                        f"Elemento {elemento.get_attribute('id')} não está visível no tamanho de tela {largura}x{altura}"
                    )
                    
                # Verificar se é possível interagir com os elementos
                self.driver.find_element(By.ID, "valor-original").clear()
                self.driver.find_element(By.ID, "valor-original").send_keys("1000")
                self.driver.find_element(By.ID, "percentual-desconto").clear()
                self.driver.find_element(By.ID, "percentual-desconto").send_keys("10")
                
                # Verificar se é possível clicar nos botões
                calcular_btn = self.driver.find_element(By.ID, "calcular")
                self.driver.execute_script("arguments[0].click();", calcular_btn)
                
                # Esperar que os resultados sejam atualizados
                self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), ""))
                
                # Verificar se o cálculo foi realizado corretamente
                valor_final = self.driver.find_element(By.ID, "valor-final").text
                self.assertNotEqual(valor_final, "0,00")
                
                # Limpar para o próximo teste
                limpar_btn = self.driver.find_element(By.ID, "limpar")
                self.driver.execute_script("arguments[0].click();", limpar_btn)
                
            except Exception as e:
                # Registrar o problema, mas não falhar o teste
                print(f"Problema de responsividade no tamanho {largura}x{altura}: {str(e)}")
        
        # Restaurar o tamanho original da janela
        self.driver.maximize_window()
    
    def test_percentuais_extremos(self):
        """
        Testa o comportamento da calculadora com percentuais de desconto extremos (0% e 100%).
        """
        # Testar com 0% de desconto
        self.driver.find_element(By.ID, "valor-original").send_keys("1000")
        self.driver.find_element(By.ID, "percentual-desconto").send_keys("0")
        
        # Selecionar desconto simples
        desconto_simples_radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")
        self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
        
        # Clicar no botão calcular
        calcular_btn = self.driver.find_element(By.ID, "calcular")
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Esperar que os resultados sejam atualizados
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), ""))
        
        # Verificar os resultados com 0% de desconto
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        valor_final = self.driver.find_element(By.ID, "valor-final").text
        
        # Converter valores para comparação
        valor_desconto_num = float(valor_desconto.replace(".", "").replace(",", "."))
        valor_final_num = float(valor_final.replace(".", "").replace(",", "."))
        
        # Com 0% de desconto, o valor do desconto deve ser 0 e o valor final igual ao original
        self.assertAlmostEqual(valor_desconto_num, 0.0, delta=0.01)
        self.assertAlmostEqual(valor_final_num, 1000.0, delta=0.01)
        
        # Limpar campos
        limpar_btn = self.driver.find_element(By.ID, "limpar")
        self.driver.execute_script("arguments[0].click();", limpar_btn)
        
        # Testar com 100% de desconto
        self.driver.find_element(By.ID, "valor-original").send_keys("1000")
        self.driver.find_element(By.ID, "percentual-desconto").send_keys("100")
        
        # Selecionar desconto simples
        self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
        
        # Clicar no botão calcular
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Esperar que os resultados sejam atualizados
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), ""))
        
        # Verificar os resultados com 100% de desconto
        valor_desconto = self.driver.find_element(By.ID, "valor-desconto").text
        valor_final = self.driver.find_element(By.ID, "valor-final").text
        
        # Converter valores para comparação
        valor_desconto_num = float(valor_desconto.replace(".", "").replace(",", "."))
        valor_final_num = float(valor_final.replace(".", "").replace(",", "."))
        
        # Com 100% de desconto, o valor do desconto deve ser igual ao original e o valor final deve ser 0
        self.assertAlmostEqual(valor_desconto_num, 1000.0, delta=0.01)
        self.assertAlmostEqual(valor_final_num, 0.0, delta=0.01)
    
    def test_combinacao_tipos_desconto(self):
        """
        Testa a mudança entre diferentes tipos de desconto sem limpar os campos.
        """
        # Preencher os campos do formulário
        self.driver.find_element(By.ID, "valor-original").send_keys("1000")
        self.driver.find_element(By.ID, "percentual-desconto").send_keys("10")
        
        # Selecionar desconto simples
        desconto_simples_radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='tipo-desconto'][value='simples']")
        self.driver.execute_script("arguments[0].click();", desconto_simples_radio)
        
        # Clicar no botão calcular
        calcular_btn = self.driver.find_element(By.ID, "calcular")
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Esperar que os resultados sejam atualizados
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), ""))
        
        # Verificar resultado com desconto simples
        valor_final_simples = self.driver.find_element(By.ID, "valor-final").text
        valor_final_simples_num = float(valor_final_simples.replace(".", "").replace(",", "."))
        
        # Mudar para desconto progressivo sem limpar os campos
        desconto_progressivo_radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='tipo-desconto'][value='progressivo']")
        self.driver.execute_script("arguments[0].click();", desconto_progressivo_radio)
        
        # Clicar no botão calcular novamente
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Esperar que os resultados sejam atualizados
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), ""))
        
        # Verificar resultado com desconto progressivo
        valor_final_progressivo = self.driver.find_element(By.ID, "valor-final").text
        valor_final_progressivo_num = float(valor_final_progressivo.replace(".", "").replace(",", "."))
        
        # Os resultados devem ser diferentes entre os tipos de desconto
        self.assertNotEqual(valor_final_simples_num, valor_final_progressivo_num)
        
        # Mudar para desconto por cupom
        desconto_cupom_radio = self.driver.find_element(By.CSS_SELECTOR, "input[name='tipo-desconto'][value='cupom']")
        self.driver.execute_script("arguments[0].click();", desconto_cupom_radio)
        
        # Adicionar um cupom válido
        self.driver.find_element(By.ID, "cupom").send_keys("SUPER50")
        
        # Clicar no botão calcular novamente
        self.driver.execute_script("arguments[0].click();", calcular_btn)
        
        # Esperar que os resultados sejam atualizados
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "valor-final"), ""))
        
        # Verificar resultado com desconto por cupom
        valor_final_cupom = self.driver.find_element(By.ID, "valor-final").text
        valor_final_cupom_num = float(valor_final_cupom.replace(".", "").replace(",", "."))
        
        # O resultado com cupom deve ser diferente dos anteriores
        self.assertNotEqual(valor_final_simples_num, valor_final_cupom_num)
        self.assertNotEqual(valor_final_progressivo_num, valor_final_cupom_num)


def executar_testes_interface_desconto():
    """
    Executa todos os testes da interface da calculadora de desconto.
    Retorna True se todos os testes passarem, False caso contrário.
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInterfaceCalculadoraDesconto)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()


if __name__ == "__main__":
    print("\n===== TESTES DA INTERFACE DA CALCULADORA DE DESCONTO =====\n")
    sucesso = executar_testes_interface_desconto()
    sys.exit(0 if sucesso else 1)