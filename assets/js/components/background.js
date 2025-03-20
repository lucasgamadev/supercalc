/**
 * Componente de fundo para SuperCalc
 * Este componente aplica o estilo de fundo gradiente em todas as páginas
 */

document.addEventListener('DOMContentLoaded', function() {
  // Verifica se o body já tem a classe de fundo
  if (!document.body.classList.contains('supercalc-background')) {
    // Aplica a classe de fundo ao body
    document.body.classList.add('supercalc-background');
  }
});