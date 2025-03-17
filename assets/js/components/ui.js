/**
 * UI Components for SuperCalc
 */

const SuperCalcUI = {
  /**
   * Creates a toast notification
   * @param {string} message - The message to display
   * @param {string} type - The type of toast (success, error, info)
   * @param {number} duration - Duration in milliseconds
   */
  showToast: function(message, type = 'info', duration = 3000) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Show with animation
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Remove after duration
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },
  
  /**
   * Format currency values (BRL)
   * @param {number} value - The value to format
   * @returns {string} Formatted currency string
   */
  formatCurrency: function(value) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SuperCalcUI;
}