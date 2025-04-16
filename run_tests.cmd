@echo off
echo Verificando e instalando dependencias necessarias...
pip install selenium
echo.
cd /d %~dp0\tests
echo Executando testes...
python interface_principal.py