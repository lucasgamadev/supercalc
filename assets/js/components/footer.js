class FooterComponent extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `
      <footer class="mt-16 text-center text-white opacity-80">
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-4 drop-shadow-lg"></h1>
        
        <!-- Botão Sobre no Footer -->
        <div class="mt-4 mb-4">
          <a href="/pages/about.html" class="inline-flex items-center bg-white bg-opacity-20 text-white px-4 py-2 rounded-full hover:bg-opacity-30 transition-all">
            <i class="fas fa-info-circle mr-2"></i>
            <span>Sobre</span>
          </a>
        </div>
        
        <p>2025 SuperCalc - Todas as calculadoras que você precisa em um só lugar</p>
      </footer>
    `;
  }
}

customElements.define('footer-component', FooterComponent);
