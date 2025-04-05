// Componente de botão de ação (apagar e copiar) do histórico de cálculos
class ActionButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  static get observedAttributes() {
    return ['icon', 'type', 'title'];
  }

  connectedCallback() {
    this.render();
    this.addEventListeners();
    // Forçar atualização do estilo
    this.updateStyles();
  }

  // Método para forçar atualização dos estilos
  updateStyles() {
    // Adicionar estilo global para os ícones
    if (!document.getElementById('action-button-global-style')) {
      const style = document.createElement('style');
      style.id = 'action-button-global-style';
      style.textContent = `
        action-button i.material-icons,
        .btn-copiar i.material-icons,
        .btn-excluir i.material-icons {
          font-size: 18px !important;
        }
      `;
      document.head.appendChild(style);
    }

    // Forçar redimensionamento em todos os botões existentes
    setTimeout(() => {
      document.querySelectorAll('action-button').forEach((btn) => {
        if (btn.shadowRoot) {
          const icon = btn.shadowRoot.querySelector('.material-icons');
          if (icon) {
            icon.style.fontSize = '18px';
          }
        }
      });
    }, 0);
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (this.isConnected && oldValue !== newValue) {
      this.render();
    }
  }

  get icon() {
    return this.getAttribute('icon') || 'touch_app';
  }

  get type() {
    return this.getAttribute('type') || 'default';
  }

  get title() {
    return this.getAttribute('title') || 'Ação';
  }

  get eventName() {
    const typeToEvent = {
      copy: 'copy-request',
      delete: 'delete-request',
    };
    return typeToEvent[this.type] || 'action';
  }

  render() {
    const buttonColor =
      this.type === 'delete'
        ? '#f44336'
        : this.type === 'copy'
          ? '#2196f3'
          : '#757575';

    const hoverBgColor =
      this.type === 'delete'
        ? 'rgba(244, 67, 54, 0.1)'
        : this.type === 'copy'
          ? 'rgba(33, 150, 243, 0.1)'
          : 'rgba(117, 117, 117, 0.1)';

    const buttonClass =
      this.type === 'delete'
        ? 'btn-excluir'
        : this.type === 'copy'
          ? 'btn-copiar'
          : 'btn-acao';

    this.shadowRoot.innerHTML = `
      <style>
        .btn-acao {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background-color: rgba(255, 255, 255, 0.9);
          border: none;
          cursor: pointer;
          transition: all 0.2s ease;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          color: ${buttonColor};
        }
        
        .btn-acao:hover {
          transform: scale(1.1);
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
          background-color: ${hoverBgColor};
        }
        
        .btn-acao:active {
          transform: scale(0.95);
        }
        
        .material-icons {
          font-family: 'Material Icons';
          font-weight: normal;
          font-style: normal;
          font-size: 18px !important;
          line-height: 1;
          letter-spacing: normal;
          text-transform: none;
          display: inline-block;
          white-space: nowrap;
          word-wrap: normal;
          direction: ltr;
          -webkit-font-smoothing: antialiased;
          text-rendering: optimizeLegibility;
          -moz-osx-font-smoothing: grayscale;
          font-feature-settings: 'liga';
        }
      </style>
      
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <button class="${buttonClass} btn-acao" title="${this.title}">
        <i class="material-icons">${this.icon}</i>
      </button>
    `;
  }

  addEventListeners() {
    const button = this.shadowRoot.querySelector('.btn-acao');
    button.addEventListener('click', () => {
      this.dispatchEvent(
        new CustomEvent(this.eventName, {
          bubbles: true,
          composed: true,
          detail: { type: this.type },
        })
      );
    });
  }
}

customElements.define('action-button', ActionButton);
