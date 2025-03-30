@echo off
setlocal enabledelayedexpansion

rem Habilitar a codificação UTF-8 para suportar caracteres acentuados e outros caracteres especiais
chcp 65001 > nul

rem Habilitar o suporte a ANSI no cmd.exe
reg add HKCU\Console /f /v VirtualTerminalLevel /t REG_DWORD /d 1 > nul

rem Sequência de cores ANSI
set "verde=[32m" & set "vermelho=[31m" & set "azul=[34m" & set "ciano=[36m" & set "magenta=[35m" & set "amarelo=[33m" & set "branco=[37m" & set "reset=[0m"

rem Array de linhas para o desenho [Apresentação]
set "line1=%azul%##################################################################################%reset%"
set "line2=%azul%##################################################################################%reset%"    
set "line3=%azul%###%verde%  _        _     _   _____   ______   _____     ____     _____ __        __ %reset%%azul%###%reset%"
set "line4=%azul%###%verde% | |      | |   | | |  ___| |  __  | /  ___|   |     \  |  ___|\ \      / / %reset%%azul%###%reset%"
set "line5=%azul%###%verde% | |      | |   | | | |     | |__| | | |___    | | \  | | |___  \ \    / /  %reset%%azul%###%reset%"
set "line6=%azul%###%verde% | |      | |   | | | |     | |  | | \___  \ ==| |  | | |  ___|  \ \  / /   %reset%%azul%###%reset%"
set "line7=%azul%###%verde% | |____  | |___| | | |___  | |  | |  ___| |   | | /  | | |___    \ \/ /    %reset%%azul%###%reset%"
set "line8=%azul%###%verde% |______| |_______| |_____| |_|  |_| |_____/   |_____/  |_____|    \__/     %reset%%azul%###%reset%"
set "line9=%azul%##################################################################################%reset%"
set "line10=%azul%##################################################################################%reset%"

rem Função para imprimir a animação
for /l %%i in (1,1,10) do (
    echo !line%%i!
    timeout /t 0 > nul
)

rem Espaçamento
echo.

rem Analizar os requisitos de sistema
echo %verde%Iniciando análise dos requisitos de sistema...%reset%
timeout /t 1 /nobreak > nul


rem Verificar qual sistema está instalado no computador (Windows 7, 8, 10 ou 11)
echo %ciano%Verificando compatibilidade do sistema operacional...%reset%
timeout /t 1 /nobreak > nul

rem Usando WMI para capturar o número da compilação
for /f "tokens=*" %%i in ('wmic os get BuildNumber ^| findstr /R /C:"[0-9]"') do (
    set "BUILD=%%i"
)

rem Exibe o número da compilação
echo Número da compilação - Build: !BUILD!
timeout /t 1 /nobreak > nul

rem Verificar a versão básica do sistema operacional
for /f "tokens=4-5 delims=[.] " %%i in ('ver') do set VERSION=%%i.%%j

rem Verificar qual versão do Windows 7, 8, 8.1 está instalada
if "%VERSION%" == "6.1" (
    echo Sistema Operacional: Windows 7.
    goto sistema-incompativel
) else if "%VERSION%" == "6.2" (
    echo Sistema Operacional: Windows 8.
    goto sistema-incompativel
) else if "%VERSION%" == "6.3" (
    echo Sistema Operacional: Windows 8.1.
    goto sistema-incompativel
) else if "%VERSION%" == "10.0" (

rem Verificar qual versão do Windows 10 ou 11 está instalada
if !BUILD! geq 22631 (
        echo Sistema Operacional: Windows 11 23H2 ou superior.
) else if !BUILD! geq 22621 (
    echo Sistema Operacional: Windows 11 22H2.
) else if !BUILD! geq 22000 (
    echo Sistema Operacional: Windows 11 21H2.
) else if !BUILD! geq 19044 (
    echo Sistema Operacional: Windows 10 21H2
) else if !BUILD! geq 19043 (
    echo Sistema Operacional: Windows 10 21H1.
) else if !BUILD! geq 19042 (
    echo Sistema Operacional: Windows 10 20H2.
) else if !BUILD! geq 19041 (
    echo Sistema Operacional: Windows 10 2004.
) else if !BUILD! geq 18363 (
    echo Sistema Operacional: Windows 10 1909.
) else if !BUILD! geq 18362 (
    echo Sistema Operacional: Windows 10 1903.
) else if !BUILD! geq 17763 (
    echo Sistema Operacional: Windows 10 1809.
) else (
    echo %vermelho%ATENÇÃO: %reset%Sistema Operacional Windows 10 com versão anterior à 1809.
    timeout /t 2 /nobreak > nul
    echo %vermelho%ATENÇÃO: %reset%Essa versão do sistema não atende aos requisitos de instalação.
    timeout /t 2 /nobreak > nul
    echo %vermelho%ATENÇÃO: %reset%Por favor, atualize seu sistema operacional para uma versão superior utilizando o %verde%Windows Update%reset%.
    timeout /t 2 /nobreak > nul
    echo %vermelho%ATENÇÃO: %reset%Requisitos de sistema: %verde%Windows 10%reset% versão %verde%1809%reset% ou superior, ou qualquer versão do %verde%Windows 11%reset%.
    pause
)
) else (
:sistema-incompativel
    echo %vermelho%ATENÇÃO: %reset%Sistema operacional não atende aos requisitos de instalação.
    timeout /t 2 /nobreak > nul
    echo %vermelho%ATENÇÃO: %reset%Requisitos de sistema: %verde%Windows 10%reset% versão %verde%1809%reset% ou superior, ou qualquer versão do %verde%Windows 11%reset%.
    pause
)

echo %verde%Requisitos de sistema atendidos.%reset%
timeout /t 1 /nobreak > nul
echo Continuando...
timeout /t 1 /nobreak > nul

rem Verificando conectividade com a internet
echo %ciano%Verificando conectividade...%reset%
timeout /t 1 /nobreak > nul
ping -n 1 google.com >nul 2>&1
if errorlevel 1 (
    echo %vermelho%Sem conexão com a Internet.%reset%
    echo %vermelho%Este script requer conexão com a Internet para instalar as dependências.%reset%
    pause
    exit /b 1
) else (
    echo %verde%Conexão com a Internet detectada.%reset%
)

rem Verificar se o winget está instalado
echo %ciano%Verificando se o winget está instalado...%reset%
winget --version >nul 2>&1
if errorlevel 1 (
    echo %vermelho%Winget não encontrado. Por favor, instale o App Installer da Microsoft Store.%reset%
    pause
    exit /b 1
) else (
    echo %verde%Winget encontrado.%reset%
)

rem Espaçamento
echo.

rem Array de linhas para o desenho [NODE]
set "line1=%azul%#########################################%reset%"
set "line2=%azul%#########################################%reset%"    
set "line3=%azul%###%verde%  _   _    ____   _____    ______  %reset%%azul%###%reset%"
set "line4=%azul%###%verde% | \ | |  / __ \ |  __ \  |  ____| %reset%%azul%###%reset%"
set "line5=%azul%###%verde% |  \| | | |  | || |  | | | |__    %reset%%azul%###%reset%"
set "line6=%azul%###%verde% | . ` | | |  | || |  | | |  __|   %reset%%azul%###%reset%"
set "line7=%azul%###%verde% | |\  | | |__| || |__| | | |____  %reset%%azul%###%reset%"
set "line8=%azul%###%verde% |_| \_|  \____/ |_____/  |______| %reset%%azul%###%reset%"
set "line9=%azul%#########################################%reset%"
set "line10=%azul%#########################################%reset%"

rem Função para imprimir a animação
for /l %%i in (1,1,10) do (
    echo !line%%i!
    timeout /t 0 > nul
)

rem Espaçamento
echo.

rem Verificar se o Node.js já consta como instalado
echo %ciano%Verificando instalação do Node.js...%reset%
echo %magenta%winget list --name "Node.js" --accept-source-agreements%reset%
winget list --name "Node.js" --accept-source-agreements
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('node --version') do (
        echo %verde%Node.js já está instalado - Versão: %%i%reset%
    )
) else (
    echo %amarelo%Node.js não encontrado. Instalando via winget...%reset%
    echo %azul%Quando solicitado, clique em %verde%Sim%reset%%azul% para instalar o Node.js.%reset%
    echo %magenta%winget install OpenJS.NodeJS --accept-source-agreements --accept-package-agreements%reset%
    winget install OpenJS.NodeJS --accept-source-agreements --accept-package-agreements
    
    echo %ciano%Aguardando o sistema registrar a instalação...%reset%
    timeout /t 5 /nobreak > nul
    
    rem Atualizar PATH sem reiniciar
    echo %ciano%Atualizando variáveis de ambiente...%reset%
    for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path ^| findstr /i "^.*Path"') do set "PATH=%%b"
    for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path ^| findstr /i "^.*Path"') do set "PATH=!PATH!;%%b"
    
    rem Verificar se a instalação foi bem sucedida  
    echo %ciano%Verificando a instalação do Node.js...%reset%  

    rem Verificar se o arquivo node.exe existe  
    if exist "C:\Program Files\nodejs\node.exe" (  
        echo %verde%Node.js instalado com sucesso.%reset%  
        rem Capturar a versão do Node.js  
        for /f "tokens=*" %%i in ('"C:\Program Files\nodejs\node.exe" --version') do (  
            echo %verde%Versão do Node.js: %%i%reset%  
        )  
    ) else (  
        echo %vermelho%Erro ao instalar Node.js. Por favor, instale manualmente.%reset%  
        pause  
        exit /b 1  
    )  
)

rem Espaçamento
echo.

rem Array de linhas para o desenho [MDLINT]
set "line1=%azul%#############################################################%reset%"
set "line2=%azul%#############################################################%reset%"    
set "line3=%azul%###%verde%  __    __  _____    _        _____   _   _   _______  %reset%%azul%###%reset%"
set "line4=%azul%###%verde% |  \  /  ||  __ \  | |      |_   _| | \ | | |__   __| %reset%%azul%###%reset%"
set "line5=%azul%###%verde% |   \/   || |  | | | |        | |   |  \| |    | |    %reset%%azul%###%reset%"
set "line6=%azul%###%verde% | |\  /| || |  | | | |        | |   | . ` |    | |    %reset%%azul%###%reset%"
set "line7=%azul%###%verde% | | \/ | || |__| | | |____   _| |_  | |\  |    | |    %reset%%azul%###%reset%"
set "line8=%azul%###%verde% |_|    |_||_____/  |______| |_____| |_| \_|    |_|    %reset%%azul%###%reset%"
set "line9=%azul%#############################################################%reset%"
set "line10=%azul%#############################################################%reset%"

rem Função para imprimir a animação
for /l %%i in (1,1,10) do (
    echo !line%%i!
    timeout /t 0 > nul
)

rem Espaçamento
echo.

rem Instalar dependências do markdownlint
echo %ciano%Instalando dependências do markdownlint...%reset%
echo %magenta%npm install --save-dev markdownlint-cli prettier --legacy-peer-deps%reset%
call npm install --save-dev markdownlint-cli prettier --legacy-peer-deps
if %errorlevel% neq 0 (
    echo %vermelho%Erro ao instalar dependências do markdownlint.%reset%
    echo %amarelo%Verifique se o Node.js está instalado corretamente e tente novamente.%reset%
    pause
    exit /b 1
) else (
    echo %verde%Dependências instaladas com sucesso.%reset%
)
echo.

rem Instalar extensão markdownlint no VS Code/Cursor
echo %verde%Instalando extensão markdownlint no VS Code/Cursor...%reset%
echo %magenta%code --install-extension DavidAnson.vscode-markdownlint%reset%
call code --install-extension DavidAnson.vscode-markdownlint
if %errorlevel% neq 0 (
    echo %vermelho%Erro ao instalar extensão markdownlint.%reset%
    echo %amarelo%Verifique se o VS Code/Cursor está instalado corretamente e tente novamente.%reset%
    pause
    exit /b 1
) else (
    echo %verde%Extensão markdownlint instalada com sucesso.%reset%
)
echo.

rem Criar arquivo .markdownlint.json se não existir
echo %ciano%Verificando arquivo de configuração .markdownlint.json...%reset%
if exist ".markdownlint.json" (
    echo %verde%Arquivo .markdownlint.json já existe, mantendo configuração atual.%reset%
) else (
    echo %ciano%Criando arquivo de configuração .markdownlint.json...%reset%
    (
    echo {
    echo   "default": true,
    echo   "MD001": true,
    echo   "MD003": { "style": "consistent" },
    echo   "MD004": { "style": "consistent" },
    echo   "MD005": true,
    echo   "MD007": { "indent": 2 },
    echo   "MD009": { "br_spaces": 2, "list_item_empty_lines": true },
    echo   "MD010": true,
    echo   "MD011": true,
    echo   "MD012": true,
    echo   "MD013": { "line_length": 120 },
    echo   "MD014": true,
    echo   "MD018": true,
    echo   "MD019": true,
    echo   "MD020": true,
    echo   "MD021": true,
    echo   "MD022": true,
    echo   "MD023": true,
    echo   "MD024": false,
    echo   "MD025": true,
    echo   "MD026": true,
    echo   "MD027": true,
    echo   "MD028": true,
    echo   "MD029": false,
    echo   "MD030": true,
    echo   "MD031": true,
    echo   "MD032": true,
    echo   "MD033": true,
    echo   "MD034": true,
    echo   "MD035": { "style": "consistent" },
    echo   "MD036": false,
    echo   "MD037": true,
    echo   "MD038": true,
    echo   "MD039": true,
    echo   "MD040": true,
    echo   "MD041": true,
    echo   "MD042": true,
    echo   "MD043": true,
    echo   "MD044": true,
    echo   "MD045": true,
    echo   "MD046": { "style": "consistent" },
    echo   "MD047": true,
    echo   "MD048": { "style": "consistent" },
    echo   "MD049": { "style": "consistent" },
    echo   "MD050": { "style": "consistent" },
    echo   "MD051": true,
    echo   "MD052": true,
    echo   "MD053": true,
    echo   "MD054": true,
    echo   "MD055": true,
    echo   "MD056": true,
    echo   "MD058": true,
    echo   "line-length": false,
    echo   "no-duplicate-heading": false,
    echo   "first-line-heading": false,
    echo   "no-multiple-blanks": false
    echo }
    ) > .markdownlint.json
    if %errorlevel% equ 0 (
        echo %verde%Arquivo .markdownlint.json criado com sucesso.%reset%
    ) else (
        echo %vermelho%Erro ao criar arquivo .markdownlint.json.%reset%
        pause
        exit /b 1
    )
)

rem Espaçamento
echo.

rem Array de linhas para o desenho [Apresentação]
set "line1=%azul%###########################################################%reset%"
set "line2=%azul%###########################################################%reset%"    
set "line3=%azul%###%verde%  ______   _____   _        _____   _   _   _______  %reset%%azul%###%reset%"
set "line4=%azul%###%verde% |  ____| /  ___| | |      |_   _| | \ | | |__   __| %reset%%azul%###%reset%"
set "line5=%azul%###%verde% | |__    | |___  | |        | |   |  \| |    | |    %reset%%azul%###%reset%"
set "line6=%azul%###%verde% |  __|   \___  \ | |        | |   | . ` |    | |    %reset%%azul%###%reset%"
set "line7=%azul%###%verde% | |____   ___| | | |____   _| |_  | |\  |    | |    %reset%%azul%###%reset%"
set "line8=%azul%###%verde% |______| |_____/ |______| |_____| |_| \_|    |_|    %reset%%azul%###%reset%"
set "line9=%azul%###########################################################%reset%"
set "line10=%azul%###########################################################%reset%"

rem Função para imprimir a animação
for /l %%i in (1,1,10) do (
    echo !line%%i!
    timeout /t 0 > nul
)

rem Espaçamento
echo.

rem Instalar dependências do ESLint
echo %ciano%Instalando dependências do ESLint...%reset%
echo %magenta%npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y eslint-config-prettier eslint-plugin-prettier prettier --legacy-peer-deps%reset%
call npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y eslint-config-prettier eslint-plugin-prettier prettier --legacy-peer-deps
if %errorlevel% neq 0 (
    echo %vermelho%Erro ao instalar dependências do ESLint.%reset%
    echo %amarelo%Verifique se o Node.js está instalado corretamente e tente novamente.%reset%
    pause
    exit /b 1
) else (
    echo %verde%Dependências instaladas com sucesso.%reset%
)
echo.

rem Instalar extensão ESLint no VS Code/Cursor
echo %Vermelho%ATENÇÃO:%reset% %verde%Para completar a configuração, instale a extensão ESLint no VS Code/Cursor:%reset%
echo %ciano%1. Abra o VS Code/Cursor%reset%
echo %ciano%2. Pressione Ctrl+Shift+X para abrir o Marketplace%reset%
echo %ciano%3. Pesquise por "ESLint"%reset%
echo %ciano%4. Clique em Instalar na extensão "ESLint" do publisher "Microsoft"%reset%
echo.
echo %amarelo%Pressione qualquer tecla para continuar com o resto da configuração...%reset%
pause > nul
echo.

rem Criar arquivo de configuração do ESLint
echo %ciano%Verificando arquivo de configuração ESLint...%reset%

rem Verificar se já existe algum arquivo de configuração do ESLint
if exist ".eslintrc.json" (
    echo %amarelo%Arquivo .eslintrc.json encontrado. Este formato não é recomendado para Node.js v20+.%reset%
    echo %ciano%Renomeando para .eslintrc.json.bak e criando nova configuração flat...%reset%
    move /y ".eslintrc.json" ".eslintrc.json.bak" > nul
)

rem Verificar se o ESLint flat config já existe
if exist "eslint.config.js" (
    echo %verde%Arquivo eslint.config.js já existe, mantendo configuração atual.%reset%
    goto skip_eslint
)

rem Atualizar o package.json para usar "type": "module" (necessário para o formato flat)
echo %ciano%Atualizando package.json para suportar ESM (necessário para configuração flat)...%reset%

rem Verificar se o arquivo package.json existe
if not exist "package.json" (
    echo %ciano%Criando arquivo package.json básico...%reset%
    (
    echo {
    echo   "name": "projeto",
    echo   "version": "1.0.0",
    echo   "description": "",
    echo   "type": "module",
    echo   "scripts": {
    echo     "lint": "eslint --config eslint.config.js ./**/*.js"
    echo   },
    echo   "devDependencies": {}
    echo }
    ) > "package.json.new"
    move /y "package.json.new" "package.json" > nul
) else (
    echo %ciano%Verificando se package.json já possui a configuração de tipo module...%reset%
    findstr /C:"\"type\": \"module\"" "package.json" > nul
    if !errorlevel! neq 0 (
        echo %ciano%Adicionando propriedade "type": "module" ao package.json...%reset%
        powershell -Command "(Get-Content package.json) -replace '\"devDependencies\": \{', '\"type\": \"module\",\n  \"scripts\": {\n    \"lint\": \"eslint --config eslint.config.js ./**/*.js\"\n  },\n  \"devDependencies\": {' | Set-Content package.json.new"
        move /y "package.json.new" "package.json" > nul
    ) else (
        echo %verde%Propriedade "type": "module" já existe no package.json.%reset%
    )
)

rem Criar arquivo eslint.config.js com configuração flat
echo %ciano%Criando novo arquivo eslint.config.js com configuração flat moderna...%reset%
(
echo import tseslint from '@typescript-eslint/eslint-plugin';
echo import tsParser from '@typescript-eslint/parser';
echo import reactPlugin from 'eslint-plugin-react';
echo import reactHooksPlugin from 'eslint-plugin-react-hooks';
echo import a11yPlugin from 'eslint-plugin-jsx-a11y';
echo import prettierPlugin from 'eslint-plugin-prettier';
echo.
echo export default [
echo   {
echo     ignores: [
echo       "*.md",
echo       "*.css",
echo       "*.html",
echo       "*.json",
echo       "*.yml",
echo       "*.yaml",
echo       "*.txt",
echo       "node_modules/",
echo       "dist/",
echo       "build/"
echo     ]
echo   },
echo   {
echo     languageOptions: {
echo       parser: tsParser,
echo       parserOptions: {
echo         ecmaFeatures: {
echo           jsx: true
echo         },
echo         ecmaVersion: 'latest',
echo         sourceType: 'module'
echo       },
echo       globals: {
echo         browser: true,
echo         es2021: true,
echo         node: true
echo       }
echo     },
echo     plugins: {
echo       '@typescript-eslint': tseslint,
echo       'react': reactPlugin,
echo       'react-hooks': reactHooksPlugin,
echo       'jsx-a11y': a11yPlugin,
echo       'prettier': prettierPlugin
echo     },
echo     rules: {
echo       'react/react-in-jsx-scope': 'off',
echo       'react/prop-types': 'off',
echo       '@typescript-eslint/explicit-module-boundary-types': 'off',
echo       '@typescript-eslint/no-explicit-any': 'warn',
echo       'prettier/prettier': [
echo         'error',
echo         {
echo           trailingComma: "none",
echo           singleQuote: false,
echo           semi: true,
echo           tabWidth: 2,
echo           printWidth: 100,
echo           endOfLine: "auto"
echo         }
echo       ]
echo     },
echo     settings: {
echo       react: {
echo         version: 'detect'
echo       }
echo     }
echo   }
echo ];
) > "eslint.config.js"

if %errorlevel% equ 0 (
    echo %verde%Arquivo eslint.config.js criado com sucesso.%reset%
) else (
    echo %vermelho%Erro ao criar arquivo eslint.config.js.%reset%
    pause
    exit /b 1
)

rem Criar arquivo .prettierrc para garantir configuração consistente
echo %ciano%Criando arquivo .prettierrc...%reset%
(
echo {
echo   "trailingComma": "none",
echo   "singleQuote": false,
echo   "semi": true,
echo   "tabWidth": 2,
echo   "printWidth": 100,
echo   "endOfLine": "auto"
echo }
) > ".prettierrc"

if %errorlevel% equ 0 (
    echo %verde%Arquivo .prettierrc criado com sucesso.%reset%
) else (
    echo %vermelho%Erro ao criar arquivo .prettierrc.%reset%
    pause
    exit /b 1
)

rem Criar arquivo .prettierignore para evitar que o Prettier formate seu próprio arquivo de configuração
echo %ciano%Criando arquivo .prettierignore...%reset%
(
echo # Ignorar o próprio arquivo de configuração do prettier
echo .prettierrc
echo .prettierrc.js
echo.
echo # Diretórios comuns para ignorar
echo node_modules/
echo dist/
echo build/
echo .git/
) > ".prettierignore"

if %errorlevel% equ 0 (
    echo %verde%Arquivo .prettierignore criado com sucesso.%reset%
) else (
    echo %vermelho%Erro ao criar arquivo .prettierignore.%reset%
    pause
    exit /b 1
)

:skip_eslint
echo.

rem Criar pasta .vscode e settings.json se não existirem
echo %ciano%Verificando pasta .vscode e arquivo settings.json...%reset%
if not exist ".vscode" (
    echo %ciano%Criando pasta .vscode...%reset%
    mkdir ".vscode"
)

rem Criar arquivo temporário com as novas configurações para comparação
echo %ciano%Preparando configurações do VS Code para ESLint flat config...%reset%
(
echo {
echo   "editor.formatOnSave": true,
echo   "editor.codeActionsOnSave": {
echo     "source.fixAll": "explicit",
echo     "source.fixAll.eslint": "explicit",
echo     "source.fixAll.format": "explicit",
echo     "source.organizeImports": "explicit",
echo     "source.addMissingImports": "explicit"
echo   },
echo   "editor.defaultFormatter": "esbenp.prettier-vscode",
echo   "[markdown]": {
echo     "editor.formatOnSave": true,
echo     "editor.defaultFormatter": "DavidAnson.vscode-markdownlint"
echo   },
echo   "markdownlint.config": {
echo     "MD024": false,
echo     "MD029": false,
echo     "MD036": false,
echo     "line-length": false,
echo     "no-duplicate-heading": false,
echo     "first-line-heading": false,
echo     "no-multiple-blanks": false
echo   },
echo   "[json]": {
echo     "editor.defaultFormatter": "esbenp.prettier-vscode"
echo   },
echo   "[jsonc]": {
echo     "editor.defaultFormatter": "esbenp.prettier-vscode"
echo   },
echo   "[ignore]": {
echo     "editor.defaultFormatter": "foxundermoon.shell-format"
echo   },
echo   "[dotenv]": {
echo     "editor.defaultFormatter": "foxundermoon.shell-format"
echo   },
echo   "[css]": {
echo     "editor.defaultFormatter": "esbenp.prettier-vscode"
echo   },
echo   "[typescript]": {
echo     "editor.defaultFormatter": "esbenp.prettier-vscode",
echo     "editor.formatOnSave": true
echo   },
echo   "[typescriptreact]": {
echo     "editor.defaultFormatter": "esbenp.prettier-vscode",
echo     "editor.formatOnSave": true,
echo     "editor.codeActionsOnSave": {
echo       "source.fixAll.eslint": "explicit"
echo     }
echo   },
echo   "[javascript]": {
echo     "editor.defaultFormatter": "esbenp.prettier-vscode",
echo     "editor.formatOnSave": true,
echo     "editor.codeActionsOnSave": {
echo       "source.fixAll.eslint": "explicit"
echo     }
echo   },
echo   "[.prettierrc.js]": {
echo     "editor.formatOnSave": false
echo   },
echo   "eslint.workingDirectories": [
echo     {
echo       "mode": "location"
echo     }
echo   ],
echo   "eslint.options": {
echo     "overrideConfigFile": "eslint.config.js"
echo   },
echo   "eslint.probe": [
echo     "javascript",
echo     "javascriptreact",
echo     "typescript",
echo     "typescriptreact"
echo   ],
echo   "eslint.codeActionsOnSave.mode": "all",
echo   "eslint.alwaysShowStatus": true,
echo   "editor.formatOnPaste": true,
echo   "editor.formatOnType": true,
echo   "typescript.tsdk": "node_modules/typescript/lib",
echo   "files.associations": {
echo     "*.md": "markdown",
echo     "*.json": "json"
echo   }
echo }
) > ".vscode\settings.json.new"

rem Verificar se o arquivo settings.json já existe
if exist ".vscode\settings.json" (
    echo %ciano%Verificando se as configurações são idênticas...%reset%
    fc /b ".vscode\settings.json" ".vscode\settings.json.new" > nul
    if !errorlevel! equ 0 (
        echo %verde%Arquivo settings.json existente já possui as configurações corretas.%reset%
        del ".vscode\settings.json.new"
        goto skip_settings
    ) else (
        echo %amarelo%Arquivo settings.json já existe com configurações diferentes. Fazendo backup...%reset%
        echo %amarelo%ATENÇÃO: Caso queira recuperar alguma configuração anterior, faça o merge manual.%reset%
        echo %ciano%Criando backup em .vscode\settings.json.bak%reset%
        copy ".vscode\settings.json" ".vscode\settings.json.bak" > nul
        if %errorlevel% equ 0 (
            echo %verde%Backup criado com sucesso.%reset%
            echo %ciano%Criando novo arquivo settings.json com configurações padrão...%reset%
        ) else (
            echo %vermelho%Erro ao criar backup. Mantendo configuração atual.%reset%
            del ".vscode\settings.json.new"
            goto skip_settings
        )
    )
)

rem Mover o arquivo temporário para o local final
move /y ".vscode\settings.json.new" ".vscode\settings.json" > nul
if %errorlevel% equ 0 (
    echo %verde%Arquivo settings.json criado com sucesso.%reset%
) else (
    echo %vermelho%Erro ao criar arquivo settings.json.%reset%
    del ".vscode\settings.json.new" 2>nul
    pause
    exit /b 1
)
:skip_settings
echo.

rem Configuração do ESLint
echo %verde%Configuração concluída, ESLint está pronto para uso.%reset%
echo %ciano%- A formatação automática está ativada ao salvar arquivos%reset%
echo %ciano%- O auto-fix do ESLint está configurado para executar ao salvar%reset%
echo %ciano%- As regras estão configuradas no formato flat em eslint.config.js%reset%
echo %ciano%- As configurações do Prettier estão em .prettierrc%reset%
echo %ciano%- O package.json foi configurado com "type": "module" para suportar o formato flat%reset%
echo %ciano%- As configurações do VS Code estão em .vscode/settings.json%reset%
echo.

rem Configuração do Markdownlint
echo %verde%Configuração concluída, Markdownlint está pronto para uso.%reset%
echo %ciano%- A formatação automática está ativada ao salvar arquivos .md%reset%
echo %ciano%- As regras estão configuradas em .markdownlint.json%reset%
echo %ciano%- As configurações do VS Code estão em .vscode/settings.json%reset%
echo.

echo.
echo %amarelo%NOTA: Se necessário, reinicie seu editor ou use a paleta de comandos (Ctrl+Shift+P) e digite 'Reload Window' para ativar as novas configurações.%reset%
echo.

rem Exibe uma mensagem de conclusão
echo %verde%Script concluído com sucesso.%reset%
timeout /t 3 /nobreak > nul

pause

endlocal