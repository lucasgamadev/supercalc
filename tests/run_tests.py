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
    try:
        from test_calculadora_juros import TestCalculadoraJuros, executar_testes
        testes_unitarios_disponiveis = True
    except ImportError:
        testes_unitarios_disponiveis = False
        print("AVISO: Módulo de testes unitários de juros não encontrado.")
    
    try:
        from test_interface_juros import TestInterfaceCalculadoraJuros, executar_testes_interface
        testes_interface_disponiveis = True
    except ImportError:
        testes_interface_disponiveis = False
        print("AVISO: Módulo de testes de interface não encontrado.")
    
    try:
        from test_historico_juros import TestHistoricoCalculadoraJuros, executar_testes_historico
        testes_historico_disponiveis = True
    except ImportError:
        testes_historico_disponiveis = False
        print("AVISO: Módulo de testes de histórico não encontrado.")
        
    try:
        from test_calculadora_desconto import TestCalculadoraDesconto, executar_testes_desconto
        testes_desconto_disponiveis = True
    except ImportError:
        testes_desconto_disponiveis = False
        print("AVISO: Módulo de testes de calculadora de desconto não encontrado.")
        
    try:
        from test_calculadora_unidades import TestCalculadoraUnidades, executar_testes_unidades
        testes_unidades_disponiveis = True
    except ImportError:
        testes_unidades_disponiveis = False
        print("AVISO: Módulo de testes de calculadora de unidades não encontrado.")
        
    try:
        from test_calculadora_padrao import TestCalculadoraPadrao, executar_testes_padrao
        testes_padrao_disponiveis = True
    except ImportError:
        testes_padrao_disponiveis = False
        print("AVISO: Módulo de testes de calculadora padrão não encontrado.")
    
    # Verificar se pelo menos um tipo de teste está disponível
    if not (testes_unitarios_disponiveis or testes_interface_disponiveis or testes_historico_disponiveis or 
            testes_desconto_disponiveis or testes_unidades_disponiveis or testes_padrao_disponiveis):
        print("ERRO: Nenhum módulo de teste foi encontrado.")
        return False
    
    # Executar testes unitários
    resultado_unitarios = True
    if testes_unitarios_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES UNITÁRIOS")
        print("=" * 80)
        resultado_unitarios = executar_testes()
        
        # Pequena pausa entre os testes para garantir que os recursos sejam liberados
        time.sleep(1)
    
    # Executar testes de interface
    resultado_interface = True
    if testes_interface_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES DE INTERFACE")
        print("=" * 80)
        resultado_interface = executar_testes_interface()
        
        # Pequena pausa entre os testes para garantir que os recursos sejam liberados
        time.sleep(1)
    
    # Executar testes de histórico
    resultado_historico = True
    if testes_historico_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES DE HISTÓRICO")
        print("=" * 80)
        resultado_historico = executar_testes_historico()
        
        # Pequena pausa entre os testes para garantir que os recursos sejam liberados
        time.sleep(1)
    
    # Executar testes de calculadora de desconto
    resultado_desconto = True
    if testes_desconto_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES DA CALCULADORA DE DESCONTO")
        print("=" * 80)
        resultado_desconto = executar_testes_desconto()
        
        # Pequena pausa entre os testes para garantir que os recursos sejam liberados
        time.sleep(1)
    
    # Executar testes de calculadora de unidades
    resultado_unidades = True
    if testes_unidades_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES DA CALCULADORA DE UNIDADES")
        print("=" * 80)
        resultado_unidades = executar_testes_unidades()
        
        # Pequena pausa entre os testes para garantir que os recursos sejam liberados
        time.sleep(1)
    
    # Executar testes de calculadora padrão
    resultado_padrao = True
    if testes_padrao_disponiveis:
        print("\n" + "=" * 80)
        print("EXECUTANDO TESTES DA CALCULADORA PADRÃO")
        print("=" * 80)
        resultado_padrao = executar_testes_padrao()
    
    # Gerar relatório consolidado
    print("\n" + "=" * 80)
    print("RELATÓRIO CONSOLIDADO DOS TESTES")
    print("=" * 80)
    
    if testes_unitarios_disponiveis:
        print(f"Testes Unitários de Juros: {'SUCESSO' if resultado_unitarios else 'FALHA'}")
    
    if testes_interface_disponiveis:
        print(f"Testes de Interface: {'SUCESSO' if resultado_interface else 'FALHA'}")
    
    if testes_historico_disponiveis:
        print(f"Testes de Histórico: {'SUCESSO' if resultado_historico else 'FALHA'}")
        
    if testes_desconto_disponiveis:
        print(f"Testes da Calculadora de Desconto: {'SUCESSO' if resultado_desconto else 'FALHA'}")
        
    if testes_unidades_disponiveis:
        print(f"Testes da Calculadora de Unidades: {'SUCESSO' if resultado_unidades else 'FALHA'}")
        
    if testes_padrao_disponiveis:
        print(f"Testes da Calculadora Padrão: {'SUCESSO' if resultado_padrao else 'FALHA'}")
    
    resultado_final = (resultado_unitarios and resultado_interface and resultado_historico and 
                      resultado_desconto and resultado_unidades and resultado_padrao)
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