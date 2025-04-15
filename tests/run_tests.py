#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para executar todos os testes automatizados do SuperCalc.

Este script executa todos os tipos de testes disponíveis:
- Testes unitários da calculadora de juros
- Testes de interface
- Testes de histórico
- Testes da calculadora de desconto
- Testes da calculadora de unidades
- Testes da calculadora padrão

E gera um relatório completo dos resultados.
"""

import os
import sys
import unittest
import importlib.util
import time


def verificar_dependencias():
    """
    Verifica se todas as dependências necessárias estão instaladas.
    Retorna True se todas as dependências estão disponíveis, False caso contrário.
    """
    dependencias = {
        'unittest': 'Módulo padrão do Python',
        'selenium': 'pip install selenium',
        'json': 'Módulo padrão do Python',
        'tempfile': 'Módulo padrão do Python',
        'shutil': 'Módulo padrão do Python',
        'math': 'Módulo padrão do Python'
    }
    
    faltando = []
    for modulo, comando in dependencias.items():
        if modulo not in ['unittest', 'json', 'tempfile', 'shutil', 'math']:  # Módulos da biblioteca padrão
            spec = importlib.util.find_spec(modulo)
            if spec is None:
                faltando.append((modulo, comando))
    
    if faltando:
        print("\n===== DEPENDÊNCIAS FALTANDO =====")
        print("Os seguintes módulos são necessários para executar todos os testes:")
        for modulo, comando in faltando:
            print(f"- {modulo}: {comando}")
        print("\nInstale as dependências acima e execute este script novamente.")
        return False
    
    return True


def executar_todos_testes():
    """
    Executa todos os testes disponíveis e gera um relatório consolidado.
    """
    # Diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    # Adicionar o diretório atual ao path para importar os módulos de teste
    sys.path.insert(0, diretorio_atual)
    
    # Importar os módulos de teste
    modulos_teste = {
        'Calculadora de Juros': ('test_calculadora_juros', 'TestCalculadoraJuros', 'executar_testes_juros'),
        'Interface de Juros': ('test_interface_juros', 'TestInterfaceCalculadoraJuros', 'executar_testes_interface_juros'),
        'Histórico de Juros': ('test_historico_juros', 'TestHistoricoCalculadoraJuros', 'executar_testes_historico_juros'),
        'Calculadora de Desconto': ('test_calculadora_desconto', 'TestCalculadoraDesconto', 'executar_testes_desconto'),
        'Calculadora de Unidades': ('test_calculadora_unidades', 'TestCalculadoraUnidades', 'executar_testes_unidades'),
        'Calculadora Padrão': ('test_calculadora_padrao', 'TestCalculadoraPadrao', 'executar_testes_padrao'),
        'Interface da Calculadora Padrão': ('test_interface_padrao', 'TestInterfaceCalculadoraPadrao', 'executar_testes_interface_padrao')
    }
    
    # Verificar quais módulos estão disponíveis
    modulos_disponiveis = {}
    for nome, (modulo, classe, funcao) in modulos_teste.items():
        try:
            importado = __import__(modulo, fromlist=[classe, funcao])
            modulos_disponiveis[nome] = (getattr(importado, classe), getattr(importado, funcao))
            print(f"Módulo de testes '{nome}' carregado com sucesso.")
        except ImportError:
            print(f"AVISO: Módulo de testes '{nome}' não encontrado.")
        except AttributeError as e:
            print(f"ERRO: Problema ao carregar '{nome}': {e}")
    
    # Verificar se pelo menos um tipo de teste está disponível
    if not modulos_disponiveis:
        print("ERRO: Nenhum módulo de teste foi encontrado.")
        return False
    
    # Executar todos os testes disponíveis
    resultados = {}
    
    for nome, (classe, funcao) in modulos_disponiveis.items():
        print("\n" + "=" * 80)
        print(f"EXECUTANDO TESTES: {nome.upper()}")
        print("=" * 80)
        resultados[nome] = funcao()
        
        # Pequena pausa entre os testes para garantir que os recursos sejam liberados
        time.sleep(1)
    
    # Gerar relatório consolidado
    print("\n" + "=" * 80)
    print("RELATÓRIO CONSOLIDADO DOS TESTES")
    print("=" * 80)
    
    for nome, resultado in resultados.items():
        print(f"Testes {nome}: {'SUCESSO' if resultado else 'FALHA'}")
    
    resultado_final = all(resultados.values())
    print("\nResultado Final: " + ("SUCESSO" if resultado_final else "FALHA"))
    
    return resultado_final


def main():
    """
    Função principal do script.
    """
    print("\n===== TESTES AUTOMATIZADOS DO SUPERCALC =====")
    
    # Verificar dependências
    if not verificar_dependencias():
        return 1
    
    # Executar todos os testes
    sucesso = executar_todos_testes()
    
    # Retornar código de saída apropriado
    return 0 if sucesso else 1


if __name__ == "__main__":
    # Criar diretório de testes se não existir
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    # Executar o script principal
    sys.exit(main())