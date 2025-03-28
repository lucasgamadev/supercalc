/**
 * Componente de Item de Histórico para SuperCalc
 * Este componente cria um item padronizado para o histórico
 * de cálculos em diferentes calculadoras.
 */

class HistoryItem extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    
    // Atributos do componente
    this.operation = this.getAttribute('operation') || '';
    this.result = this.getAttribute('result') || '';
    this.operatorType = this.getAttribute('operator-type') || 'default'; // soma, subtracao, multiplicacao, divisao, porcentagem, default
    this.resultClass = this.getAttribute('result-class') || 'resultado-positivo'; // resultado-positivo, resultado-zero, resultado-negativo
  }

  connectedCallback() {
    this.render();
    this.addEventListeners();
  }

  static get observedAttributes() {
    return ['operation', 'result', 'operator-type', 'result-class'];
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (oldValue !== newValue) {
      switch (name) {
        case 'operation':
          this.operation = newValue;
          break;
        case 'result':
          this.result = newValue;
          break;
        case 'operator-type':
          this.operatorType = newValue;
          break;
        case 'result-class':
          this.resultClass = newValue;
          break;
      }
      if (this.shadowRoot) {
        this.render();
      }
    }
  }

  getOperatorIcon() {
    let iconContent = '';
    let operadorClasse = '';
    
    switch (this.operatorType) {
      case 'soma':
        operadorClasse = 'operador-soma';
        iconContent = '<span style="color: white; font-size: 16px; font-weight: bold;">+</span>';
        break;
      case 'subtracao':
        operadorClasse = 'operador-subtracao';
        iconContent = '<span style="color: white; font-size: 16px; font-weight: bold;">−</span>';
        break;
      case 'multiplicacao':
        operadorClasse = 'operador-multiplicacao';
        iconContent = '<span style="color: white; font-size: 16px; font-weight: bold;">×</span>';
        break;
      case 'divisao':
        operadorClasse = 'operador-divisao';
        iconContent = '<span style="color: white; font-size: 16px; font-weight: bold;">÷</span>';
        break;
      case 'porcentagem':
        operadorClasse = 'operador-porcentagem';
        iconContent = '<span style="color: white; font-size: 16px; font-weight: bold;">%</span>';
        break;
      default:
        operadorClasse = '';
        iconContent = '<i class="material-icons" style="color: white; font-size: 16px;">calculate</i>';
        break;
    }
    
    return `<div class="symbol-container ${operadorClasse}">${iconContent}</div>`;
  }

  getOperatorColor() {
    switch (this.operatorType) {
      case 'soma': return '#4caf50'; // Verde para adição
      case 'subtracao': return '#f44336'; // Vermelho para subtração
      case 'multiplicacao': return '#ff9800'; // Laranja para multiplicação
      case 'divisao': return '#9c27b0'; // Roxo para divisão
      case 'porcentagem': return '#00bcd4'; // Ciano para porcentagem
      default: return '#2196f3'; // Azul padrão
    }
  }

  render() {
    const operatorColor = this.getOperatorColor();
    const iconContent = this.getOperatorIcon();
    
    this.shadowRoot.innerHTML = `
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
      <style>
        :host {
          display: block;
          margin-bottom: 15px;
        }
        
        .resultado-item {
          position: relative;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 10px 15px;
          background: linear-gradient(145deg, rgba(255, 255, 255, 0.51), rgba(250, 250, 250, 0.51));
          border-radius: 12px;
          transition: all 0.3s ease;
          border-left: 4px solid ${operatorColor};
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
          transform-origin: center;
          font-family: "Roboto", sans-serif;
          animation: fadeIn 0.3s ease-in-out;
        }

        .resultado-item:hover {
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
          transform: translateY(-1px) scale(1.005);
        }

        .historico-conteudo {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 1;
        }

        .historico-expressao {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 1rem;
          color: #333;
          font-weight: 500;
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

        .resultado-item:hover .symbol-container {
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .operador-soma { background: linear-gradient(to bottom, #4caf50, #8bc34a); }
        .operador-subtracao { background: linear-gradient(to bottom, #f44336, #ff5252); }
        .operador-multiplicacao { background: linear-gradient(to bottom, #ff9800, #ffb74d); }
        .operador-divisao { background: linear-gradient(to bottom, #9c27b0, #ba68c8); }
        .operador-porcentagem { background: linear-gradient(to bottom, #00bcd4, #4dd0e1); }

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

        .btn-copiar {
          background: transparent;
          border: none;
          cursor: pointer;
          color: #757575;
          padding: 4px;
          border-radius: 4px;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .btn-copiar:hover {
          background-color: rgba(0, 0, 0, 0.05);
          color: #333;
        }
        
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      </style>
      <div class="resultado-item">
        <div class="historico-conteudo">
          ${iconContent}
          <span>${this.operation} =</span>
          <span class="resultado-valor ${this.resultClass}">${this.result}</span>
        </div>
        <button class="btn-copiar" title="Copiar resultado">
          <i class="material-icons" style="font-size: 18px;">content_copy</i>
        </button>
      </div>
    `;
  }

  addEventListeners() {
    const btnCopiar = this.shadowRoot.querySelector('.btn-copiar');
    if (btnCopiar) {
      btnCopiar.addEventListener('click', (e) => {
        e.stopPropagation();
        this.copiarParaAreaDeTransferencia(this.result);
      });
    }
  }

  /**
   * Copia o resultado para a área de transferência
   * @param {string} texto - O texto a ser copiado
   */
  copiarParaAreaDeTransferencia(texto) {
    navigator.clipboard.writeText(texto)
      .then(() => {
        // Dispara um evento personalizado para notificar que o texto foi copiado
        this.dispatchEvent(new CustomEvent('copy-success', {
          bubbles: true,
          composed: true,
          detail: { message: 'Resultado copiado para a área de transferência!' }
        }));
      })
      .catch((err) => {
        console.error('Erro ao copiar: ', err);
        this.dispatchEvent(new CustomEvent('copy-error', {
          bubbles: true,
          composed: true,
          detail: { message: 'Não foi possível copiar o resultado.' }
        }));
      });
  }
}

// Registra o componente
customElements.define('history-item', HistoryItem);