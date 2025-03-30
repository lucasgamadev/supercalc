/**
 * Componente de Botão Limpar Histórico para SuperCalc
 * Este componente cria um botão reutilizável para limpar o histórico
 * de cálculos em diferentes calculadoras.
 */

class ClearHistoryButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.storageKey = this.getAttribute('storage-key') || 'historico';
    this.historyListId =
      this.getAttribute('history-list-id') || 'historico-list';
    this.historyContainerId =
      this.getAttribute('container-id') || 'historico-container';
    this.successMessage =
      this.getAttribute('success-message') || 'Histórico limpo com sucesso!';
    this.emptyMessage =
      this.getAttribute('empty-message') || 'O histórico já está vazio!';
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
          background: linear-gradient(135deg, #ff9800, #ff5722);
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
          width: auto;
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
      </style>
      <button class="btn waves-effect waves-light orange" aria-label="Limpar histórico">
        <i class="material-icons left" aria-hidden="true">delete_sweep</i>
        <slot>Limpar Histórico</slot>
      </button>
    `;
  }

  addEventListeners() {
    const button = this.shadowRoot.querySelector('.btn');
    button.addEventListener('click', () => this.limparHistorico());
  }

  /**
   * Limpa o histórico de cálculos
   */
  limparHistorico() {
    const historico = document.getElementById(this.historyListId);
    const historicoContainer = document.getElementById(this.historyContainerId);

    // Verifica se o histórico já está vazio
    if (!historico || historico.children.length === 0) {
      this.showToast(this.emptyMessage, 'rounded orange');
      return;
    }

    // Remove todos os itens do histórico
    while (historico.firstChild) {
      historico.removeChild(historico.firstChild);
    }

    // Remove do localStorage se um storageKey foi fornecido
    if (this.storageKey) {
      localStorage.removeItem(this.storageKey);
    }

    // Adiciona o componente EmptyHistory para indicar que o histórico está vazio
    const emptyHistory = document.createElement('empty-history');
    emptyHistory.setAttribute('message', 'Nenhum cálculo no histórico');
    emptyHistory.setAttribute(
      'sub-message',
      'Os cálculos realizados aparecerão aqui'
    );
    historico.appendChild(emptyHistory);

    // Mostra o container de histórico se especificado
    if (historicoContainer) {
      historicoContainer.classList.add('show');
    }

    this.showToast(this.successMessage, 'rounded green');
  }

  /**
   * Exibe uma notificação toast
   * @param {string} message - Mensagem a ser exibida
   * @param {string} classes - Classes CSS para o toast
   */
  showToast(message, classes) {
    // Usa o componente ToastNotification se disponível
    if (
      typeof ToastNotification !== 'undefined' &&
      ToastNotification.showToast
    ) {
      ToastNotification.showToast(message, classes, 2000);
    } else if (typeof M !== 'undefined' && M.toast) {
      // Fallback para Materialize se ToastNotification não estiver disponível
      M.toast({
        html: message,
        classes: `${classes} center-align`,
        displayLength: 1000,
      });
    } else {
      // Fallback final
      alert(message);
    }
  }
}

// Registra o componente
customElements.define('clear-history-button', ClearHistoryButton);
