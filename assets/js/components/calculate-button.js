/**
 * Componente de Botão Calcular para SuperCalc
 * Este componente cria um botão reutilizável para realizar cálculos
 * em diferentes calculadoras da aplicação.
 */

class CalculateButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.text = this.getAttribute('text') || 'Calcular';
    this.icon = this.getAttribute('icon') || 'calculate';
    this.color = this.getAttribute('color') || 'blue';
    this.onClick = this.getAttribute('onclick') || '';
  }

  connectedCallback() {
    this.render();
    this.addEventListeners();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
      <style>
        .btn {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, var(--primary-color, #2196f3), var(--secondary-color, #00bcd4));
          color: white;
          border: none;
          border-radius: 6px;
          padding: 0 16px;
          height: 36px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          box-shadow: 0 3px 5px rgba(0, 0, 0, 0.2);
          transition: all 0.3s ease;
          font-family: "Roboto", sans-serif;
          width: 100%;
          position: relative;
          overflow: hidden;
        }
        
        .btn:hover {
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
          transform: translateY(-1px);
        }
        
        .btn:active {
          transform: translateY(1px);
          box-shadow: 0 2px 3px rgba(0, 0, 0, 0.2);
        }
        
        .btn::before {
          content: '';
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: rgba(255, 255, 255, 0.1);
          transform: rotate(45deg);
          animation: shimmer 2s infinite;
          pointer-events: none;
        }
        
        @keyframes shimmer {
          0% {
            transform: translate(-50%, -50%) rotate(45deg);
          }
          100% {
            transform: translate(50%, 50%) rotate(45deg);
          }
        }
        
        .material-icons {
          font-size: 18px !important;
          margin-right: 4px;
        }
        
        .btn.blue {
          --primary-color: #2196f3;
          --secondary-color: #00bcd4;
        }
        
        .btn.green {
          --primary-color: #4caf50;
          --secondary-color: #8bc34a;
        }
        
        .btn.orange {
          --primary-color: #ff9800;
          --secondary-color: #ffc107;
        }
        
        .btn.red {
          --primary-color: #f44336;
          --secondary-color: #ff5722;
        }
        
        .btn.purple {
          --primary-color: #9c27b0;
          --secondary-color: #673ab7;
        }
        
        /* Responsividade */
        @media (max-width: 480px) {
          .btn {
            height: 34px;
            font-size: 13px;
          }
          
          .material-icons {
            font-size: 16px !important;
          }
        }
        
        @media (max-width: 320px) {
          .btn {
            height: 32px;
            font-size: 12px;
          }
          
          .material-icons {
            font-size: 14px !important;
          }
        }
      </style>
      <button class="btn ${this.color} waves-effect waves-light" aria-label="${this.text}">
        <i class="material-icons left" aria-hidden="true">${this.icon}</i>
        <slot>${this.text}</slot>
      </button>
    `;
  }

  addEventListeners() {
    const button = this.shadowRoot.querySelector('.btn');
    button.addEventListener('click', (event) => {
      // Disparar um evento personalizado que pode ser capturado pela página
      const customEvent = new CustomEvent('calculate', {
        bubbles: true,
        composed: true,
        detail: { source: this },
      });
      this.dispatchEvent(customEvent);

      // Se houver um onclick definido, executá-lo
      if (this.onClick) {
        // Usar eval com cuidado - apenas para compatibilidade com código existente
        // Em uma implementação ideal, seria melhor usar apenas eventos personalizados
        eval(this.onClick);
      }
    });
  }

  // Observa mudanças nos atributos
  static get observedAttributes() {
    return ['text', 'icon', 'color', 'onclick'];
  }

  // Responde a mudanças de atributos
  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      switch (name) {
        case 'text':
          this.text = newValue;
          break;
        case 'icon':
          this.icon = newValue;
          break;
        case 'color':
          this.color = newValue;
          break;
        case 'onclick':
          this.onClick = newValue;
          break;
      }
      this.render();
    }
  }
}

// Registra o componente
customElements.define('calculate-button', CalculateButton);
