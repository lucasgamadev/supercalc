/**
 * Componente de Botão Início para SuperCalc
 * Este componente cria um botão reutilizável para navegação
 * para a página inicial em diferentes partes da aplicação.
 */

class HomeButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.href = this.getAttribute('href') || '/index.html';
    this.text = this.getAttribute('text') || 'Início';
    this.icon = this.getAttribute('icon') || 'fa-home';
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
      <style>
        :host {
          display: block;
          margin: 0 auto;
          text-align: center;
        }
        .nav-btn {
          display: inline-flex;
          align-items: center;
          background: linear-gradient(to right, var(--primary-color, #2196f3), var(--secondary-color, #00bcd4));
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 9999px;
          font-size: 0.875rem;
          font-weight: 500;
          text-decoration: none;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          transition: all 0.3s ease;
          margin: 0 auto;
        }
        
        .nav-btn:hover {
          opacity: 0.9;
          transform: translateY(-1px);
        }
        
        .nav-btn:active {
          transform: translateY(1px);
          box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
        }
        
        .icon {
          margin-right: 0.5rem;
          display: inline-flex;
          align-items: center;
        }
      </style>
      <a href="${this.href}" class="nav-btn" title="Ir para a página inicial">
        <span class="icon"><i class="fas ${this.icon}"></i></span>
        <slot>${this.text}</slot>
      </a>
    `;
  }

  /**
   * Atualiza o atributo href do botão
   * @param {string} href - O novo href para o botão
   */
  setHref(href) {
    this.href = href;
    const button = this.shadowRoot.querySelector('.nav-btn');
    if (button) {
      button.setAttribute('href', href);
    }
  }

  /**
   * Atualiza o texto do botão
   * @param {string} text - O novo texto para o botão
   */
  setText(text) {
    this.text = text;
    this.render();
  }

  /**
   * Atualiza o ícone do botão
   * @param {string} icon - O novo ícone para o botão (classe FontAwesome)
   */
  setIcon(icon) {
    this.icon = icon;
    this.render();
  }

  // Observa mudanças nos atributos
  static get observedAttributes() {
    return ['href', 'text', 'icon'];
  }

  // Responde a mudanças de atributos
  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      switch (name) {
        case 'href':
          this.href = newValue;
          break;
        case 'text':
          this.text = newValue;
          break;
        case 'icon':
          this.icon = newValue;
          break;
      }
      this.render();
    }
  }
}

// Registra o componente
customElements.define('home-button', HomeButton);
