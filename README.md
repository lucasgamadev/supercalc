# 🧮 SuperCalc

Uma coleção de calculadoras úteis para diversas finalidades.

## Estrutura do Projeto

```text
/
├── index.html
├── assets/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── main.js
│   │   └── components/
│   │       └── ui.js
│   ├── images/
│   │   └── logo.svg
│   └── fonts/
├── components/
│   └── header.html
├── pages/
│   └── about.html
├── tailwind.config.js
├── package.json
└── README.md
```

## 🧮 Calculadoras Disponíveis

- **💰 Calculadora de Desconto**: Calcule rapidamente o valor final após aplicar um desconto.

## 🛠️ Tecnologias Utilizadas

- 🟠 HTML5
- 🔵 CSS3 & 🌊 TailwindCSS
- 🟡 JavaScript

## 🚀 Como Executar

1. Clone este repositório
2. Abra o arquivo `index.html` em seu navegador

Ou rode um servidor local com prévia e recarregamento automático:

```bash
# Servir o projeto e abrir a prévia no navegador (http://127.0.0.1:5500)
npx live-server --port=5500 --open=index.html
```

## 👨‍💻 Desenvolvimento

Para trabalhar no desenvolvimento do projeto:

```bash
# Instalar dependências
npm install

# Executar em modo de desenvolvimento (com watch)
npm run dev

# Gerar build para produção
npm run build

# Verificar o código com ESLint
npm run lint

# Corrigir problemas de lint automaticamente
npm run lint:fix
```
