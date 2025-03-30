/**
 * Componente de Histórico Vazio para SuperCalc
 * Este componente cria uma mensagem padronizada para quando o histórico
 * de cálculos estiver vazio em diferentes calculadoras.
 */

class EmptyHistory extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.message =
      this.getAttribute('message') ||
      'Nenhum registro encontrado no histórico.';
    this.subMessage =
      this.getAttribute('sub-message') ||
      'Os registros salvos aparecerão aqui.';
  }

  connectedCallback() {
    this.render();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        .empty-history-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 20px;
          text-align: center;
          color: #757575;
          font-family: "Roboto", sans-serif;
          animation: fadeIn 0.5s ease-in-out;
        }
        
        .icon {
          font-size: 48px;
          margin-bottom: 16px;
          color: #9e9e9e;
          opacity: 0.7;
        }
        
        .message {
          font-size: 16px;
          font-weight: 500;
          margin-bottom: 8px;
        }
        
        .sub-message {
          font-size: 14px;
          opacity: 0.8;
        }
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      </style>
      <div class="empty-history-container">
        <div class="icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
        </div>
        <div class="message">${this.message}</div>
        <div class="sub-message">${this.subMessage}</div>
      </div>
    `;
  }

  /**
   * Atualiza as mensagens do componente
   * @param {string} message - Mensagem principal
   * @param {string} subMessage - Mensagem secundária
   */
  updateMessages(message, subMessage) {
    if (message) this.message = message;
    if (subMessage) this.subMessage = subMessage;
    this.render();
  }
}

// Registra o componente
customElements.define('empty-history', EmptyHistory);
