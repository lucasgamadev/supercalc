class HistoryItem extends HTMLElement {
  constructor() {
    super();
    // Cria Shadow DOM
    this.attachShadow({ mode: 'open' });
    // Inicializa propriedades
    this.operation = '';
    this.result = '';
    this.resultClass = 'resultado-positivo';
    this.operatorType = 'default';
    
    // Importa o componente de botu00e3o de au00e7u00e3o se ainda nu00e3o estiver registrado
    if (!customElements.get('action-button')) {
      const script = document.createElement('script');
      script.src = '/assets/js/components/action-button.js';
      document.head.appendChild(script);
    }
  }
  // Ciclo de vida: quando o componente é adicionado ao DOM
  connectedCallback() {
    this.render();
    this.addEventListeners();
  }
  // Define quais atributos devem ser observados
  static get observedAttributes() {
    return ['operation', 'result', 'result-class', 'operator-type'];
  }
  // Ciclo de vida: quando um atributo observado é alterado
  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      switch (name) {
        case 'operation':
          this.operation = newValue;
          break;
        case 'result':
          this.result = newValue;
          break;
        case 'result-class':
          this.resultClass = newValue;
          break;
        case 'operator-type':
          this.operatorType = newValue;
          break;
      }
      // Apenas renderiza novamente se o componente já estiver no DOM
      if (this.isConnected) {
        this.render();
      }
    }
  }
  // Renderiza o conteúdo no Shadow DOM
  render() {
    // Determina qual ícone será exibido com base no tipo de operador
    let iconContent = '';
    let operadorCor = '#2196f3'; // Azul padrão
    let operadorClasse = '';
    switch (this.operatorType) {
      case 'soma':
        iconContent =
          '<div class="symbol-container operador-soma"><span style="color: white; font-size: 16px; font-weight: bold;">+</span></div>';
        operadorCor = '#4caf50'; // Verde para adição
        operadorClasse = 'operador-soma';
        break;
      case 'subtracao':
        iconContent =
          '<div class="symbol-container operador-subtracao"><span style="color: white; font-size: 16px; font-weight: bold;">−</span></div>';
        operadorCor = '#f44336'; // Vermelho para subtração
        operadorClasse = 'operador-subtracao';
        break;
      case 'multiplicacao':
        iconContent =
          '<div class="symbol-container operador-multiplicacao"><span style="color: white; font-size: 16px; font-weight: bold;">×</span></div>';
        operadorCor = '#ff9800'; // Laranja para multiplicação
        operadorClasse = 'operador-multiplicacao';
        break;
      case 'divisao':
        iconContent =
          '<div class="symbol-container operador-divisao"><span style="color: white; font-size: 16px; font-weight: bold;">÷</span></div>';
        operadorCor = '#9c27b0'; // Roxo para divisão
        operadorClasse = 'operador-divisao';
        break;
      case 'porcentagem':
        iconContent =
          '<div class="symbol-container operador-porcentagem"><span style="color: white; font-size: 16px; font-weight: bold;">%</span></div>';
        operadorCor = '#00bcd4'; // Ciano para porcentagem
        operadorClasse = 'operador-porcentagem';
        break;
      case 'conversao-moeda':
        iconContent =
          '<div class="symbol-container operador-conversao"><i class="material-icons" style="color: white; font-size: 18px;">currency_exchange</i></div>';
        operadorCor = '#3f51b5'; // Índigo
        break;
      case 'juros-simples':
        iconContent =
          '<div class="symbol-container operador-juros-simples"><i class="material-icons" style="color: white; font-size: 18px;">percent</i></div>';
        operadorCor = '#009688'; // Teal
        break;
      case 'juros-compostos':
        iconContent =
          '<div class="symbol-container operador-juros-compostos"><i class="material-icons" style="color: white; font-size: 18px;">analytics</i></div>';
        operadorCor = '#673ab7'; // Deep Purple
        break;
      case 'desconto':
        iconContent =
          '<div class="symbol-container operador-desconto"><i class="material-icons" style="color: white; font-size: 18px;">discount</i></div>';
        operadorCor = '#e91e63'; // Pink
        break;
      default:
        iconContent =
          '<div class="symbol-container" style="background: linear-gradient(to bottom, #2196f3, #64b5f6);"><i class="material-icons" style="color: white; font-size: 18px;">calculate</i></div>';
        operadorCor = '#2196f3'; // Azul padrão
        break;
    }
    // Estilo e HTML do componente
    this.shadowRoot.innerHTML = `
      <!-- Importação dos ícones do Material Design para o Shadow DOM -->
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <style>
        .resultado-item {
          position: relative;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 10px 12px;
          background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.85),
            rgba(250, 250, 250, 0.85)
          );
          border-radius: 12px;
          transition: all 0.3s ease;
          border-left: 4px solid ${operadorCor};
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
          margin-bottom: 8px;
          transform-origin: center;
          font-family: 'Roboto', sans-serif;
        }

        .resultado-item:hover {
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
        }

        .historico-conteudo {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 1;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .historico-expressao {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 1rem;
          color: #333;
          font-weight: 500;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 100%;
        }

        .historico-expressao::before {
          content: '';
          display: none;
        }

        .resultado-valor {
          font-weight: 600;
          display: inline-block;
          position: relative;
          padding: 2px 8px;
          border-radius: 4px;
          transition: all 0.3s ease;
        }

        .resultado-positivo {
          color: #4caf50;
          background-color: rgba(76, 175, 80, 0.1);
        }

        .resultado-zero {
          color: #757575;
          background-color: rgba(117, 117, 117, 0.1);
        }

        .resultado-negativo {
          color: #f44336;
          background-color: rgba(244, 67, 54, 0.1);
        }

        .resultado-valor:hover {
          transform: scale(1.05);
        }

        .resultado-positivo:hover {
          background-color: rgba(76, 175, 80, 0.2);
        }

        .resultado-zero:hover {
          background-color: rgba(117, 117, 117, 0.2);
        }

        .resultado-negativo:hover {
          background-color: rgba(244, 67, 54, 0.2);
        }

        .acoes-container {
          display: flex;
          gap: 8px;
        }

        .btn-copiar, .btn-excluir {
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
        }

        .btn-copiar {
          color: #2196f3;
        }

        .btn-excluir {
          color: #f44336;
        }
        
        .btn-excluir .material-icons {
          font-size: 20px !important; /* Aumentado de 18px para 20px */
        }
        
        .btn-copiar:hover, .btn-excluir:hover {
          transform: scale(1.1);
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
        }

        .btn-copiar:hover {
          background-color: rgba(33, 150, 243, 0.1);
        }

        .btn-excluir:hover {
          background-color: rgba(244, 67, 54, 0.1);
        }

        .btn-copiar:active, .btn-excluir:active {
          transform: scale(0.95);
        }

        /* Estilos para os ícones do Material Design */
        .material-icons {
          font-family: 'Material Icons';
          font-weight: normal;
          font-style: normal;
          font-size: 18px;
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

        .symbol-container {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 26px;
          height: 26px;
          border-radius: 6px;
          margin-right: 8px;
          position: relative;
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
          text-align: center;
          transition: box-shadow 0.2s ease;
        }

        .operador-soma {
          background: linear-gradient(to bottom, #4caf50, #8bc34a);
        }
        .operador-subtracao {
          background: linear-gradient(to bottom, #f44336, #ff5252);
        }
        .operador-multiplicacao {
          background: linear-gradient(to bottom, #ff9800, #ffb74d);
        }
        .operador-divisao {
          background: linear-gradient(to bottom, #9c27b0, #ba68c8);
        }
        .operador-porcentagem {
          background: linear-gradient(to bottom, #00bcd4, #4dd0e1);
        }
        .operador-conversao {
          background: linear-gradient(to bottom, #3f51b5, #7986cb);
        }
        .operador-juros-simples {
          background: linear-gradient(to bottom, #009688, #4db6ac);
        }
        .operador-juros-compostos {
          background: linear-gradient(to bottom, #673ab7, #9575cd);
        }
        .operador-desconto {
          background: linear-gradient(to bottom, #e91e63, #f48fb1);
        }
        
        /* Animação de entrada */
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        :host {
          display: block;
          animation: fadeIn 0.3s ease-out;
        }
      </style>

      <div class="resultado-item">
        <div class="historico-conteudo">
          ${iconContent}
          <span class="historico-expressao">${this.operation} =</span>
          <span class="resultado-valor ${this.resultClass}">${this.result}</span>
        </div>
        <div class="acoes-container">
          <action-button type="copy" icon="content_copy" title="Copiar resultado"></action-button>
          <action-button type="delete" icon="delete_outline" title="Excluir do histórico"></action-button>
        </div>
      </div>
    `;
  }
  // Adiciona event listeners
  addEventListeners() {
    const actionButtons = this.shadowRoot.querySelectorAll('action-button');
    actionButtons.forEach(button => {
      if (button.getAttribute('type') === 'copy') {
        button.addEventListener('copy-request', this.copiarResultado.bind(this));
      } else if (button.getAttribute('type') === 'delete') {
        button.addEventListener('delete-request', this.excluirItem.bind(this));
      }
    });
  }
  // Função para copiar o resultado para a área de transferência
  copiarResultado() {
    const resultado = this.result;
    // Usa a API Clipboard para copiar o texto
    navigator.clipboard
      .writeText(resultado)
      .then(() => {
        // Dispara um evento personalizado para notificar que o texto foi copiado
        this.dispatchEvent(
          new CustomEvent('copy-success', {
            bubbles: true,
            composed: true,
            detail: {
              message: 'Resultado copiado para a área de transferência!',
            },
          })
        );
      })
      .catch((err) => {
        console.error('Erro ao copiar: ', err);
        this.dispatchEvent(
          new CustomEvent('copy-error', {
            bubbles: true,
            composed: true,
            detail: { message: 'Não foi possível copiar o resultado.' },
          })
        );
      });
  }

  // Função para excluir o item do histórico
  excluirItem() {
    // Dispara um evento personalizado para notificar que o item deve ser excluído
    this.dispatchEvent(
      new CustomEvent('delete-item', {
        bubbles: true,
        composed: true,
        detail: {
          operation: this.operation,
          result: this.result,
        },
      })
    );
  }
}
// Registra o componente
customElements.define('history-item', HistoryItem);
