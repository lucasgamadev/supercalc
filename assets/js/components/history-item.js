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

    switch (this.operatorType) {
      case 'conversao-moeda':
        iconContent =
          '<i class="material-icons" style="font-size: 18px;">currency_exchange</i>';

        break;

      case 'juros-simples':
        iconContent =
          '<i class="material-icons" style="font-size: 18px;">percent</i>';

        break;

      case 'juros-compostos':
        iconContent =
          '<i class="material-icons" style="font-size: 18px;">analytics</i>';

        break;

      case 'desconto':
        iconContent =
          '<i class="material-icons" style="font-size: 18px;">discount</i>';

        break;

      default:
        iconContent =
          '<i class="material-icons" style="font-size: 18px;">calculate</i>';

        break;
    }

    // Estilo e HTML do componente

    this.shadowRoot.innerHTML = `

      <style>

        .resultado-item {

          font-family: 'Roboto', sans-serif;

          background-color: #f7f7f7;

          padding: 12px 16px;

          border-radius: 8px;

          margin-bottom: 10px;

          display: flex;

          justify-content: space-between;

          align-items: center;

          transition: background-color 0.2s, transform 0.2s;

          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

          border-left: 4px solid #ddd;

        }

        

        .resultado-item:hover {

          background-color: #f0f0f0;

          transform: translateY(-2px);

          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);

        }

        

        .historico-conteudo {

          display: flex;

          align-items: center;

          flex-grow: 1;

          min-width: 0; /* Para permitir que o texto seja truncado */

        }

        

        .historico-conteudo i {

          margin-right: 8px;

          color: #666;

        }

        

        .historico-conteudo span {

          white-space: nowrap;

          overflow: hidden;

          text-overflow: ellipsis;

          margin-right: 10px;

          font-size: 14px;

          color: #333;

        }

        

        .resultado-valor {

          font-weight: bold;

          padding: 3px 8px;

          border-radius: 4px;

          margin-left: auto;

        }

        

        .resultado-positivo {

          color: #28a745;

          background-color: rgba(40, 167, 69, 0.1);

        }

        

        .resultado-negativo {

          color: #dc3545;

          background-color: rgba(220, 53, 69, 0.1);

        }

        

        .resultado-zero {

          color: #6c757d;

          background-color: rgba(108, 117, 125, 0.1);

        }

        

        .btn-copiar {

          background: transparent;

          border: none;

          cursor: pointer;

          color: #6c757d;

          margin-left: 8px;

          padding: 4px;

          border-radius: 4px;

          display: flex;

          align-items: center;

          justify-content: center;

          transition: background-color 0.2s, color 0.2s;

        }

        

        .btn-copiar:hover {

          background-color: #e9ecef;

          color: #495057;

        }

        

        .btn-copiar:focus {

          outline: none;

          box-shadow: 0 0 0 2px rgba(108, 117, 125, 0.25);

        }

        

        .btn-copiar i {

          font-size: 16px;

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

          <span>${this.operation}</span>

          <span class="resultado-valor ${this.resultClass}">${this.result}</span>

        </div>

        <button class="btn-copiar" title="Copiar resultado">

          <i class="material-icons" style="font-size: 18px;">content_copy</i>

        </button>

      </div>

    `;
  }

  // Adiciona event listeners

  addEventListeners() {
    const btnCopiar = this.shadowRoot.querySelector('.btn-copiar');

    if (btnCopiar) {
      btnCopiar.addEventListener('click', this.copiarResultado.bind(this));
    }
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
}

// Registra o componente

customElements.define('history-item', HistoryItem);
