/**
 * Componente de Header para SuperCalc
 * Este componente cria um cabeçalho reutilizável para todas as páginas
 * da aplicação SuperCalc.
 */

class HeaderComponent extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
      
      <style>
        :host {
          display: block;
          width: 100%;
          margin-top: -15px;
          margin-bottom: 15px;
        }
        
        header {
          text-align: center;
          padding-bottom: 10px;
        }
        
        h1 {
          font-size: 2.5rem;
          font-weight: bold;
          color: white;
          margin-bottom: 1rem;
          text-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
          font-family: 'Roboto', sans-serif;
        }
        
        @media (min-width: 768px) {
          h1 {
            font-size: 3rem;
          }
        }
        
        p {
          font-size: 1.25rem;
          color: white;
          opacity: 0.9;
          max-width: 36rem;
          margin: 0 auto;
          font-family: 'Roboto', sans-serif;
        }
        
        i {
          margin-right: 0.5rem;
        }
      </style>
      
      <header>
        <h1><i class="fas fa-calculator"></i>SuperCalc</h1>
        <p>Uma coleção de calculadoras úteis para diversas finalidades</p>
      </header>
    `;
  }
}

// Registra o componente
customElements.define('header-component', HeaderComponent); 