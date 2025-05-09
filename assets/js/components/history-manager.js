/**
 * Gerenciador de Histórico para SuperCalc
 * Este módulo fornece funções para gerenciar o histórico de cálculos
 * de forma padronizada em todas as calculadoras.
 */

class HistoryManager {
  /**
   * Inicializa o gerenciador de histórico
   * @param {string} storageKey - Chave para armazenamento no localStorage
   * @param {string} historyListId - ID do elemento HTML que contém a lista de histórico
   * @param {string} historyContainerId - ID do container do histórico
   */
  constructor(storageKey, historyListId, historyContainerId) {
    this.storageKey = storageKey;
    this.historyListId = historyListId;
    this.historyContainerId = historyContainerId;
    this.historyList = document.getElementById(historyListId);
    this.historyContainer = document.getElementById(historyContainerId);
  }

  /**
   * Adiciona um item ao histórico
   * @param {string} operation - A operação realizada (ex: "2 + 2")
   * @param {string} result - O resultado da operação (ex: "4")
   * @param {string} operatorType - O tipo de operador (soma, subtracao, multiplicacao, divisao, porcentagem, desconto, default)
   */
  addHistoryItem(operation, result, operatorType = 'default') {
    // Verifica se existe o componente EmptyHistory e remove se existir
    const emptyHistory = this.historyList.querySelector('empty-history');
    if (emptyHistory) {
      this.historyList.removeChild(emptyHistory);
    }

    // Determina a classe do resultado com base no valor
    let resultClass = 'resultado-positivo';
    const numericValue = parseFloat(result.toString().replace(',', '.'));
    if (numericValue === 0) {
      resultClass = 'resultado-zero';
    } else if (numericValue < 0) {
      resultClass = 'resultado-negativo';
    }

    // Cria o componente de item de histórico
    const historyItem = document.createElement('history-item');
    historyItem.setAttribute('operation', operation);
    historyItem.setAttribute('result', result);
    historyItem.setAttribute('operator-type', operatorType);
    historyItem.setAttribute('result-class', resultClass);

    // Adiciona o item ao início da lista
    this.historyList.prepend(historyItem);

    // Adiciona evento para ouvir quando o item for copiado
    historyItem.addEventListener('copy-success', (e) => {
      this.showToast(e.detail.message, 'green rounded');
    });

    historyItem.addEventListener('copy-error', (e) => {
      this.showToast(e.detail.message, 'red rounded');
    });

    // Adiciona evento para ouvir quando o item for excluído
    historyItem.addEventListener('delete-item', (e) => {
      this.deleteHistoryItem(e.detail.operation, e.detail.result);
    });

    // Armazena no localStorage
    this.saveHistoryItem({
      operation,
      result,
      operatorType,
      resultClass,
    });

    // Mostra o container de histórico
    this.historyContainer.classList.add('show');
  }

  /**
   * Salva um item no histórico do localStorage
   * @param {Object} item - O item a ser salvo
   */
  saveHistoryItem(item) {
    const items = this.getSavedHistory() || [];
    items.unshift(JSON.stringify(item)); // Adiciona no início do array

    // Limita o número de itens no histórico
    if (items.length > 30) {
      items.pop(); // Remove o último item
    }

    localStorage.setItem(this.storageKey, JSON.stringify(items));
  }

  /**
   * Obtém o histórico salvo no localStorage
   * @returns {Array} - Array com os itens do histórico
   */
  getSavedHistory() {
    const history = localStorage.getItem(this.storageKey);
    return history ? JSON.parse(history) : null;
  }

  /**
   * Verifica se um item do histórico é válido
   * @param {Object} item - O item a ser validado
   * @returns {boolean} - True se o item for válido, false caso contrário
   */
  isValidHistoryItem(item) {
    // Verifica se o item contém as propriedades necessárias
    if (!item || typeof item !== 'object') return false;

    // Verifica se as propriedades esperadas existem e são do tipo correto
    if (typeof item.operation !== 'string' || typeof item.result !== 'string') {
      return false;
    }

    // Verifica se a operação ou resultado contém HTML (possível indicador de corrupção)
    if (item.operation.includes('<') || item.result.includes('<')) {
      return false;
    }

    // Verifica se o resultado é um número válido
    const numericValue = parseFloat(item.result.toString().replace(',', '.'));
    if (isNaN(numericValue)) {
      return false;
    }

    return true;
  }

  /**
   * Carrega o histórico do localStorage
   */
  loadHistory() {
    const items = this.getSavedHistory();
    if (items && items.length > 0) {
      this.historyContainer.classList.add('show');
      let validItemCount = 0;

      // Mostra todos os itens do histórico
      items.forEach((itemString) => {
        try {
          const item = JSON.parse(itemString);

          // Verifica se o item é válido antes de renderizá-lo
          if (!this.isValidHistoryItem(item)) {
            console.warn(
              'Item inválido de histórico encontrado e ignorado:',
              item
            );
            return; // Pula este item
          }

          validItemCount++;

          // Cria o componente de item de histórico
          const historyItem = document.createElement('history-item');
          historyItem.setAttribute('operation', item.operation);
          historyItem.setAttribute('result', item.result);
          historyItem.setAttribute(
            'operator-type',
            item.operatorType || 'default'
          );
          historyItem.setAttribute(
            'result-class',
            item.resultClass || 'resultado-positivo'
          );

          // Adiciona o item à lista
          this.historyList.appendChild(historyItem);

          // Adiciona evento para ouvir quando o item for copiado
          historyItem.addEventListener('copy-success', (e) => {
            this.showToast(e.detail.message, 'green rounded');
          });

          historyItem.addEventListener('copy-error', (e) => {
            this.showToast(e.detail.message, 'red rounded');
          });

          // Adiciona evento para ouvir quando o item for excluído
          historyItem.addEventListener('delete-item', (e) => {
            this.deleteHistoryItem(e.detail.operation, e.detail.result);
          });
        } catch (e) {
          console.error('Erro ao carregar item do histórico:', e);
        }
      });

      // Se não houver itens válidos, exibe mensagem de histórico vazio
      if (validItemCount === 0) {
        this.showEmptyHistory();
      }
    } else {
      this.showEmptyHistory();
    }
  }

  /**
   * Exibe o componente de histórico vazio
   */
  showEmptyHistory() {
    // Mostra o componente de histórico vazio
    this.historyList.innerHTML = '';
    const emptyHistory = document.createElement('empty-history');
    emptyHistory.setAttribute('message', 'Nenhum cálculo no histórico');
    emptyHistory.setAttribute(
      'sub-message',
      'Os cálculos realizados aparecerão aqui'
    );
    this.historyList.appendChild(emptyHistory);

    // Adiciona um pequeno atraso para garantir que o componente seja renderizado antes de mostrar o container
    setTimeout(() => {
      this.historyContainer.classList.add('show');
    }, 100);
  }

  /**
   * Limpa o histórico
   */
  clearHistory() {
    // Verifica se o histórico já está vazio
    if (!this.historyList || this.historyList.children.length === 0) {
      this.showToast('O histórico já está vazio!', 'orange rounded');
      return;
    }

    // Remove todos os itens do histórico
    this.historyList.innerHTML = '';
    localStorage.removeItem(this.storageKey);

    // Adiciona o componente de histórico vazio
    const emptyHistory = document.createElement('empty-history');
    emptyHistory.setAttribute('message', 'Nenhum cálculo no histórico');
    emptyHistory.setAttribute(
      'sub-message',
      'Os cálculos realizados aparecerão aqui'
    );
    this.historyList.appendChild(emptyHistory);

    this.historyContainer.classList.add('show');
    this.showToast('Histórico limpo com sucesso!', 'green rounded');
  }

  /**
   * Exclui um item específico do histórico
   * @param {string} operation - A operação do item a ser excluído
   * @param {string} result - O resultado do item a ser excluído
   */
  deleteHistoryItem(operation, result) {
    // Obtém o histórico atual
    const items = this.getSavedHistory() || [];
    if (items.length === 0) return;

    // Encontra o item a ser excluído
    const updatedItems = items.filter((itemString) => {
      try {
        const item = JSON.parse(itemString);
        // Verifica se é o item que queremos excluir
        return !(item.operation === operation && item.result === result);
      } catch (e) {
        console.error('Erro ao processar item do histórico:', e);
        return true; // Mantém itens com erro
      }
    });

    // Atualiza o localStorage
    if (updatedItems.length === 0) {
      localStorage.removeItem(this.storageKey);
    } else {
      localStorage.setItem(this.storageKey, JSON.stringify(updatedItems));
    }

    // Remove o elemento do DOM
    const historyItems = this.historyList.querySelectorAll('history-item');
    historyItems.forEach((item) => {
      if (
        item.getAttribute('operation') === operation &&
        item.getAttribute('result') === result
      ) {
        item.remove();
      }
    });

    // Verifica se o histórico ficou vazio
    if (this.historyList.children.length === 0) {
      this.showEmptyHistory();
    }

    // Mostra mensagem de sucesso
    this.showToast('Item removido do histórico!', 'green rounded');
  }

  /**
   * Detecta o tipo de operador com base na expressão
   * @param {string} operation - A operação a ser analisada
   * @returns {string} - O tipo de operador
   */
  static detectOperatorType(operation) {
    if (operation.includes('+')) {
      return 'soma';
    } else if (operation.includes('−') || operation.includes('-')) {
      return 'subtracao';
    } else if (operation.includes('×') || operation.includes('*')) {
      return 'multiplicacao';
    } else if (operation.includes('÷') || operation.includes('/')) {
      return 'divisao';
    } else if (operation.includes('%')) {
      return 'porcentagem';
    }

    return 'default';
  }

  /**
   * Mostra uma mensagem toast
   * @param {string} message - A mensagem a ser exibida
   * @param {string} classes - Classes CSS para o toast
   */
  showToast(message, classes = 'rounded') {
    // Verifica se o componente ToastNotification existe
    if (typeof ToastNotification !== 'undefined') {
      // Usa o método estático do componente ToastNotification
      ToastNotification.showToast(message, classes);
    } else {
      // Fallback para o Materialize Toast se o componente não estiver disponível
      if (typeof M !== 'undefined' && M.toast) {
        M.toast({ html: message, classes: classes });
      } else {
        console.log(message);
      }
    }
  }
}

// Exporta a classe para uso em outros arquivos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = HistoryManager;
} else {
  // Para uso no navegador
  window.HistoryManager = HistoryManager;
}
