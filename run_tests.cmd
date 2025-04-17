@echo off
echo Iniciando servidor HTTP na porta 8080...
start "Servidor HTTP" cmd /k python -m http.server 8080

REM Aguarda alguns segundos para garantir que o servidor está ativo
ping 127.0.0.1 -n 4 > nul

echo Verificando e instalando dependencias necessarias...
pip install selenium
echo.
cd /d %~dp0\tests
echo Executando testes...
python interface_principal.py