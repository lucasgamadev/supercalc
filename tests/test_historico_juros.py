import unittest
import os
import sys
import json
import tempfile
import shutil

class TestHistoricoCalculadoraJuros(unittest.TestCase):
    """
    Testes automatizados para validar a funcionalidade de histórico da calculadora de juros.
    Estes testes verificam se o histórico é salvo e recuperado corretamente.
    """
    
    def setUp(self):
        """
        Configuração inicial para cada teste.
        Cria um ambiente simulado para testar o histórico.
        """
        # Criar um diretório temporário para simular o localStorage
        self.temp_dir = tempfile.mkdtemp()
        self.storage_file = os.path.join(self.temp_dir, 'local_storage.json')
        
        # Inicializar o storage vazio
        self.storage = {}
        self.save_storage()
    
    def tearDown(self):
        """
        Limpeza após cada teste.
        """
        # Remover o diretório temporário
        shutil.rmtree(self.temp_dir)
    
    def save_storage(self):
        """
        Salva o storage simulado em um arquivo JSON.
        """
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.storage, f)
    
    def load_storage(self):
        """
        Carrega o storage simulado de um arquivo JSON.
        """
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                self.storage = json.load(f)
        else:
            self.storage = {}
    
    def simular_history_manager(self):
        """
        Simula o comportamento da classe HistoryManager do JavaScript.
        """
        class HistoryManagerSimulado:
            def __init__(self, storage_key, storage_dict, storage_file):
                self.storage_key = storage_key
                self.storage = storage_dict
                self.storage_file = storage_file
            
            def add_history_item(self, operation, result, operator_type='default'):
                # Criar um item de histórico
                item = {
                    'operation': operation,
                    'result': result,
                    'operatorType': operator_type
                }
                
                # Obter o histórico atual
                items = self.get_saved_history() or []
                
                # Adicionar o novo item no início
                items.insert(0, json.dumps(item))
                
                # Limitar o número de itens
                if len(items) > 30:
                    items.pop()
                
                # Salvar no storage
                self.storage[self.storage_key] = json.dumps(items)
                
                # Salvar no arquivo
                with open(self.storage_file, 'w', encoding='utf-8') as f:
                    json.dump(self.storage, f)
                
                return item
            
            def get_saved_history(self):
                # Carregar do storage
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.storage = json.load(f)
                
                # Obter o histórico
                history_json = self.storage.get(self.storage_key)
                if history_json:
                    return json.loads(history_json)
                return []
            
            def clear_history(self):
                # Limpar o histórico
                self.storage[self.storage_key] = json.dumps([])
                
                # Salvar no arquivo
                with open(self.storage_file, 'w', encoding='utf-8') as f:
                    json.dump(self.storage, f)
        
        return HistoryManagerSimulado('calculo-juros-historico', self.storage, self.storage_file)
    
    def test_adicionar_item_historico(self):
        """
        Testa a adição de um item ao histórico.
        """
        # Criar o gerenciador de histórico simulado
        history_manager = self.simular_history_manager()
        
        # Adicionar um item ao histórico
        item = history_manager.add_history_item(
            'Valor: R$ 1.000,00 | Taxa: 10% | Período: 12 meses | Tipo: Simples',
            'R$ 2.200,00',
            'juros-simples'
        )
        
        # Verificar se o item foi adicionado corretamente
        historico = history_manager.get_saved_history()
        self.assertEqual(len(historico), 1)
        
        # Verificar o conteúdo do item
        item_salvo = json.loads(historico[0])
        self.assertEqual(item_salvo['operation'], 'Valor: R$ 1.000,00 | Taxa: 10% | Período: 12 meses | Tipo: Simples')
        self.assertEqual(item_salvo['result'], 'R$ 2.200,00')
        self.assertEqual(item_salvo['operatorType'], 'juros-simples')
    
    def test_limite_itens_historico(self):
        """
        Testa se o histórico respeita o limite de 30 itens.
        """
        # Criar o gerenciador de histórico simulado
        history_manager = self.simular_history_manager()
        
        # Adicionar 35 itens ao histórico
        for i in range(35):
            history_manager.add_history_item(
                f'Cálculo {i}',
                f'Resultado {i}',
                'juros-simples'
            )
        
        # Verificar se o histórico tem no máximo 30 itens
        historico = history_manager.get_saved_history()
        self.assertEqual(len(historico), 30)
        
        # Verificar se os itens mais recentes foram mantidos
        item_mais_recente = json.loads(historico[0])
        self.assertEqual(item_mais_recente['operation'], 'Cálculo 34')
        
        # Verificar se os itens mais antigos foram removidos
        item_mais_antigo = json.loads(historico[-1])
        self.assertEqual(item_mais_antigo['operation'], 'Cálculo 5')
    
    def test_limpar_historico(self):
        """
        Testa a limpeza do histórico.
        """
        # Criar o gerenciador de histórico simulado
        history_manager = self.simular_history_manager()
        
        # Adicionar alguns itens ao histórico
        for i in range(5):
            history_manager.add_history_item(
                f'Cálculo {i}',
                f'Resultado {i}',
                'juros-simples'
            )
        
        # Verificar se os itens foram adicionados
        historico = history_manager.get_saved_history()
        self.assertEqual(len(historico), 5)
        
        # Limpar o histórico
        history_manager.clear_history()
        
        # Verificar se o histórico foi limpo
        historico = history_manager.get_saved_history()
        self.assertEqual(len(historico), 0)
    
    def test_persistencia_historico(self):
        """
        Testa se o histórico persiste entre sessões.
        """
        # Criar o primeiro gerenciador de histórico
        history_manager1 = self.simular_history_manager()
        
        # Adicionar alguns itens ao histórico
        for i in range(3):
            history_manager1.add_history_item(
                f'Cálculo {i}',
                f'Resultado {i}',
                'juros-simples'
            )
        
        # Simular o fechamento e reabertura da aplicação
        # criando um novo gerenciador de histórico
        history_manager2 = self.simular_history_manager()
        
        # Verificar se o histórico foi mantido
        historico = history_manager2.get_saved_history()
        self.assertEqual(len(historico), 3)
        
        # Verificar o conteúdo do histórico
        for i in range(3):
            item = json.loads(historico[2-i])
            self.assertEqual(item['operation'], f'Cálculo {i}')
            self.assertEqual(item['result'], f'Resultado {i}')


def executar_testes_historico():
    """
    Executa os testes de histórico e exibe um relatório detalhado.
    """
    print("\n===== TESTES AUTOMATIZADOS DO HISTÓRICO DA CALCULADORA DE JUROS =====\n")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHistoricoCalculadoraJuros)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\n===== RESUMO DOS TESTES DE HISTÓRICO =====")
    print(f"Total de testes: {resultado.testsRun}")
    print(f"Testes com sucesso: {resultado.testsRun - len(resultado.failures) - len(resultado.errors)}")
    print(f"Falhas: {len(resultado.failures)}")
    print(f"Erros: {len(resultado.errors)}")
    
    if resultado.failures or resultado.errors:
        print("\n===== DETALHES DAS FALHAS =====")
        for test, error in resultado.failures:
            print(f"\nTeste: {test}")
            print(f"Erro: {error}")
        
        print("\n===== DETALHES DOS ERROS =====")
        for test, error in resultado.errors:
            print(f"\nTeste: {test}")
            print(f"Erro: {error}")
    
    return len(resultado.failures) == 0 and len(resultado.errors) == 0


if __name__ == "__main__":
    # Criar diretório de testes se não existir
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    # Executar testes
    sucesso = executar_testes_historico()
    
    # Retornar código de saída apropriado
    sys.exit(0 if sucesso else 1)