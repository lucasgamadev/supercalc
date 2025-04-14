#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script principal para executar todos os testes automatizados da calculadora de juros do SuperCalc.

Este script executa todos os tipos de testes disponíveis:
- Testes unitários de cálculos
- Testes de interface
- Testes de histórico

E gera um relatório consolidado dos resultados.
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
        'shutil': 'Módulo padrão do Python'
    }
    
    faltando = []
    for modulo, comando in dependencias.items():
        if modulo not in ['unittest', 'json', 'tempfile', 'shutil']:  # Módulos da biblioteca padrão
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
        'Unitários': ('test_calculadora_juros', 'TestCalculadoraJuros', 'executar_testes'),
        'Interface': ('test_interface_juros', 'TestInterfaceCalculadoraJuros', 'executar_testes_interface'),
        'Histórico': ('test_historico_juros', 'TestHistoricoCalculadoraJuros', 'executar_testes_historico')
    }
    
    testes_disponiveis = {}
    for nome, (modulo, classe, funcao) in modulos_teste.items():
        try:
            mod = importlib.import_module(modulo)
            testes_disponiveis[nome] = getattr(mod, funcao)
        except (ImportError, AttributeError):
            print(f"AVISO: Módulo de testes {nome} não encontrado ou função executar não disponível.")
    
    # Verificar se pelo menos um tipo de teste está disponível
    if not testes_disponiveis:
        print("ERRO: Nenhum módulo de teste foi encontrado.")
        return False
    
    # Executar todos os testes disponíveis
    resultados = {}
    for nome, funcao in testes_disponiveis.items():
        print("\n" + "=" * 80)
        print(f"EXECUTANDO TESTES {nome.upper()}")
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
    print("\n===== TESTES AUTOMATIZADOS DA CALCULADORA DE JUROS DO SUPERCALC =====")
    
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