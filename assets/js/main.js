/**
 * Arquivo JavaScript principal para SuperCalc
 */

// Importar componentes
import '/assets/js/components/background.js';

document.addEventListener('DOMContentLoaded', function() {
  // Inicializar componentes globais ou funcionalidades
  console.log('SuperCalc initialized');
  
  // Animação para o cabeçalho
  setTimeout(() => {
    const header = document.querySelector('header');
    if (header) {
      header.style.opacity = '0';
      header.style.transform = 'translateY(-20px)';
      header.style.transition = 'all 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      
      setTimeout(() => {
        header.style.opacity = '1';
        header.style.transform = 'translateY(0)';
      }, 100);
    }
  }, 100);
  
  // Animação para os cards
  const cards = document.querySelectorAll('.calculator-card');
  cards.forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(40px) scale(0.95)';
    
    setTimeout(() => {
      card.style.transition = 'all 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
      card.style.opacity = '1';
      card.style.transform = 'translateY(0) scale(1)';
    }, 300 + (150 * index)); // Efeito escalonado com mais tempo entre cada card
  });
  
  // Animação para o footer
  const footer = document.querySelector('footer');
  if (footer) {
    footer.style.opacity = '0';
    setTimeout(() => {
      footer.style.transition = 'opacity 1s ease';
      footer.style.opacity = '1';
    }, 1000);
  }
  
  // Adicionar event listeners para navegação com efeito de clique
  const navLinks = document.querySelectorAll('a.calculator-card');
  if (navLinks) {
    navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        // Efeito de clique
        e.preventDefault();
        const href = this.getAttribute('href');
        
        this.style.transform = 'scale(0.95)';
        this.style.opacity = '0.8';
        
        setTimeout(() => {
          window.location.href = href;
        }, 300);
      });
    });
  }
});