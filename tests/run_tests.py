#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para executar todos os testes automatizados da calculadora de juros do SuperCalc.

Este script executa tanto os testes unitários quanto os testes de interface,
gerando um relatório completo dos resultados.
"""

import os
import sys
import unittest
import importlib.util


def verificar_dependencias():
    """
    Verifica se todas as dependências necessárias estão instaladas.
    Retorna True se todas as dependências estão disponíveis, False caso contrário.
    """
    dependencias = {
        'unittest': 'Módulo padrão do Python',
        'selenium': 'pip install selenium',
    }
    
    faltando = []
    for modulo, comando in dependencias.items():
        if modulo != 'unittest':  # unittest é parte da biblioteca padrão
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
    try:
        from test_calculadora_juros import TestCalculadoraJuros, executar_testes
        testes_unitarios_disponiveis = True
    except ImportError:
        testes_unitarios_disponiveis = False
        print("AVISO: Módulo de testes unitários não encontrado.")
    
    try:
        from test_interface_juros import TestInterfaceCalculadoraJuros, executar_testes_interface
        testes_interface_disponiveis = True
    except ImportError:
        testes_interface_disponiveis = False
        print("AVISO: Módulo de testes de interface não encontrado.")
    
    # Verificar se pelo menos um tipo de teste está disponível
    if not testes_unitarios_disponiveis and not testes_interface_disponiveis:
        print("ERRO: Nenhum módulo de teste foi encontrado.")
        return False
    
    # Executar testes unitários
    resultado_unitarios = True
    if testes_unitarios_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES UNITÁRIOS")
        print("=" * 80)
        resultado_unitarios = executar_testes()
    
    # Executar testes de interface
    resultado_interface = True
    if testes_interface_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES DE INTERFACE")
        print("=" * 80)
        resultado_interface = executar_testes_interface()
    
    # Gerar relatório consolidado
    print("\n" + "=" * 80)
    print("RELATÓRIO CONSOLIDADO DOS TESTES")
    print("=" * 80)
    
    if testes_unitarios_disponiveis:
        print(f"Testes Unitários: {'SUCESSO' if resultado_unitarios else 'FALHA'}")
    
    if testes_interface_disponiveis:
        print(f"Testes de Interface: {'SUCESSO' if resultado_interface else 'FALHA'}")
    
    resultado_final = resultado_unitarios and resultado_interface
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