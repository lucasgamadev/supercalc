# Testes Automatizados da Calculadora de Juros

Este diretório contém testes automatizados para validar a calculadora de juros do SuperCalc. Os testes verificam tanto a lógica de cálculo quanto a interface do usuário.

## Estrutura dos Testes

O sistema de testes está organizado da seguinte forma:

- `test_calculadora_juros.py`: Testes unitários para validar os cálculos matemáticos de juros simples e compostos.
- `test_interface_juros.py`: Testes de interface que simulam a interação do usuário com a calculadora.
- `run_tests.py`: Script principal para executar todos os testes e gerar relatórios.

## Requisitos

Para executar os testes, você precisa ter instalado:

1. Python 3.6 ou superior
2. Selenium WebDriver (para testes de interface)
3. Navegador Chrome ou Firefox
4. ChromeDriver ou GeckoDriver (compatível com a versão do seu navegador)

### Instalação de Dependências

```bash
pip install selenium
```

### Configuração do WebDriver

Para os testes de interface, você precisa ter o ChromeDriver ou GeckoDriver instalado e disponível no PATH do sistema. Você pode baixá-los em:

- ChromeDriver: [Download ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- GeckoDriver: [Download GeckoDriver](https://github.com/mozilla/geckodriver/releases)

## Executando os Testes

### Todos os Testes

Para executar todos os testes disponíveis:

```bash
python run_tests.py
```

### Apenas Testes Unitários

Para executar apenas os testes unitários (sem abrir o navegador):

```bash
python test_calculadora_juros.py
```

### Apenas Testes de Interface

Para executar apenas os testes de interface (abrirá o navegador):

```bash
python test_interface_juros.py
```

## Interpretando os Resultados

Após a execução dos testes, você verá um relatório detalhado com os seguintes componentes:

- Total de testes executados
- Número de testes bem-sucedidos
- Número de falhas e erros
- Detalhes de cada falha ou erro (se houver)

Um teste bem-sucedido indica que a calculadora está funcionando conforme o esperado para o cenário testado.

## Casos de Teste

### Testes Unitários

1. **Juros Simples**: Verifica se o cálculo de juros simples está correto para diferentes valores de entrada.
2. **Juros Compostos**: Verifica se o cálculo de juros compostos está correto para diferentes valores de entrada.
3. **Classificação de Taxa**: Verifica se a classificação da taxa de juros (baixa, média, alta) está correta.
4. **Formatação de Moeda**: Verifica se a formatação de valores monetários no padrão brasileiro está correta.

### Testes de Interface

1. **Cálculo de Juros Simples**: Verifica se a interface calcula corretamente os juros simples.
2. **Cálculo de Juros Compostos**: Verifica se a interface calcula corretamente os juros compostos.
3. **Validação de Campos**: Verifica se a validação de campos obrigatórios está funcionando.
4. **Limpar Campos**: Verifica se o botão de limpar campos está funcionando corretamente.

## Manutenção dos Testes

Se a interface ou a lógica de cálculo da calculadora for modificada, os testes podem precisar ser atualizados. Certifique-se de manter os testes sincronizados com as mudanças no código da aplicação.

## Solução de Problemas

### Testes de Interface Falham

Se os testes de interface estiverem falhando, verifique:

1. Se o navegador Chrome ou Firefox está instalado
2. Se o ChromeDriver ou GeckoDriver está instalado e no PATH
3. Se a versão do driver é compatível com a versão do navegador
4. Se a estrutura HTML da página não foi alterada (IDs, classes, etc.)

### Testes Unitários Falham

Se os testes unitários estiverem falhando, verifique:

1. Se a lógica de cálculo na aplicação foi alterada
2. Se as fórmulas nos testes correspondem às fórmulas na aplicação
3. Se há problemas de arredondamento ou precisão numérica
