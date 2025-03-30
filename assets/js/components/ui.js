/**
 * Componentes de UI para SuperCalc
 */

const SuperCalcUI = {
  /**
   * Cria uma notificação toast
   * @param {string} message - A mensagem a ser exibida
   * @param {string} type - O tipo do toast (sucesso, erro, info)
   * @param {number} duration - Duração em milissegundos
   */
  showToast: function (message, type = 'info', duration = 3000) {
    // Criar elemento toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    // Adicionar ao documento
    document.body.appendChild(toast);

    // Mostrar com animação
    setTimeout(() => toast.classList.add('show'), 10);

    // Remover após a duração
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  /**
   * Formata valores monetários (BRL)
   * @param {number} valor - O valor a ser formatado
   * @returns {string} Valor formatado em moeda brasileira (BRL)
   */
  formatCurrency: function (value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(value);
  },
};

// Exportar para uso em outros arquivos
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SuperCalcUI;
}
