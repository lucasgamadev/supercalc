/**
 * Componente de Notificação Toast para SuperCalc
 * Este componente cria um sistema de notificações reutilizável
 * para exibir mensagens ao usuário em diferentes partes da aplicação.
 */

class ToastNotification extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });

    // Configurações padrão
    this.duration = parseInt(this.getAttribute('duration')) || 2000;
    this.position = this.getAttribute('position') || 'center';
    this.containerId = 'toast-container';
  }

  connectedCallback() {
    this.render();
    this.setupContainer();
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
        }
        
        #toast-container {
          display: flex !important;
          justify-content: center !important;
          align-items: center !important;
          position: fixed !important;
          top: 50% !important;
          left: 50% !important;
          transform: translate(-50%, -50%) !important;
          width: auto !important;
          max-width: none !important;
          height: auto !important;
          pointer-events: none;
          z-index: 10000;
        }
        
        .toast {
          min-width: 200px;
          padding: 12px 24px;
          color: white;
          border-radius: 8px;
          margin: 8px auto;
          font-size: 16px;
          font-weight: 500;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          text-align: center;
          opacity: 0;
          transform: translateY(20px);
          transition: opacity 0.3s, transform 0.3s;
          pointer-events: auto;
          max-width: 80%;
        }
        
        .toast.show {
          opacity: 1;
          transform: translateY(0);
        }
        
        .toast.rounded {
          border-radius: 24px;
        }
        
        .toast.red {
          background: linear-gradient(135deg, #e53935, #ef5350);
        }
        
        .toast.green {
          background: linear-gradient(135deg, #43a047, #66bb6a);
        }
        
        .toast.blue {
          background: linear-gradient(135deg, #1e88e5, #42a5f5);
        }
        
        .toast.orange {
          background: linear-gradient(135deg, #fb8c00, #ffa726);
        }
        
        /* Ajuste para diferentes tamanhos de tela */
        @media (max-width: 480px) {
          #toast-container {
            width: 90% !important;
            left: 5% !important;
            transform: translateY(-50%) !important;
          }

          .toast {
            font-size: 14px !important;
            padding: 10px 15px !important;
            width: 100% !important;
          }
        }
      </style>
      <slot></slot>
    `;
  }

  /**
   * Configura o container de toast se não existir
   */
  setupContainer() {
    if (!document.getElementById(this.containerId)) {
      const container = document.createElement('div');
      container.id = this.containerId;

      // Aplicar estilos diretamente ao criar o container com !important
      container.style.cssText = `
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        pointer-events: none !important;
        z-index: 10000 !important;
      `;

      document.body.appendChild(container);
    }
  }

  /**
   * Exibe uma notificação toast
   * @param {string} message - Mensagem a ser exibida
   * @param {string} classes - Classes CSS para o toast (ex: 'rounded green')
   * @param {number} duration - Duração em milissegundos
   */
  show(message, classes = 'rounded', duration = this.duration) {
    // Remove toasts anteriores
    const existingToasts = document.querySelectorAll('.toast');
    existingToasts.forEach((toast) => toast.remove());

    // Cria o elemento toast
    const toast = document.createElement('div');
    toast.className = `toast ${classes}`;
    toast.innerHTML = message;

    // Adiciona ao container
    const container = document.getElementById(this.containerId);
    if (container) {
      container.appendChild(toast);
      // Reforça os estilos com !important a cada exibição
      container.style.cssText = `
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        pointer-events: none !important;
        z-index: 10000 !important;
      `;

      // Mostra com animação
      setTimeout(() => toast.classList.add('show'), 10);

      // Remove após a duração
      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
          toast.remove();
          // Se não houver mais toasts, esconde o container
          if (container.children.length === 0) {
            container.style.display = 'none';
          }
        }, 300);
      }, duration);
    }
  }

  /**
   * Método estático para mostrar toast sem precisar instanciar o componente
   * @param {string} message - Mensagem a ser exibida
   * @param {string} classes - Classes CSS para o toast
   * @param {number} duration - Duração em milissegundos
   */
  static showToast(message, classes = 'rounded', duration = 2000) {
    // Verifica se o componente já foi registrado
    if (!customElements.get('toast-notification')) {
      customElements.define('toast-notification', ToastNotification);
    }

    // Cria uma instância temporária se não existir no DOM
    let toastComponent = document.querySelector('toast-notification');
    if (!toastComponent) {
      toastComponent = document.createElement('toast-notification');
      document.body.appendChild(toastComponent);
    }

    // Garante que o container de toast exista e esteja configurado corretamente
    const containerId = 'toast-container';
    let container = document.getElementById(containerId);

    if (!container) {
      container = document.createElement('div');
      container.id = containerId;
      document.body.appendChild(container);
    }

    // Reforça os estilos com !important para garantir centralização
    container.style.cssText = `
      display: flex !important;
      justify-content: center !important;
      align-items: center !important;
      position: fixed !important;
      top: 50% !important;
      left: 50% !important;
      transform: translate(-50%, -50%) !important;
      width: 100% !important;
      max-width: 100% !important;
      height: auto !important;
      pointer-events: none !important;
      z-index: 10000 !important;
    `;

    // Exibe o toast
    toastComponent.show(message, classes, duration);
  }
}

// Registra o componente
customElements.define('toast-notification', ToastNotification);
