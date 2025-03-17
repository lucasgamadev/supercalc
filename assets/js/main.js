/**
 * Main JavaScript file for SuperCalc
 */

document.addEventListener('DOMContentLoaded', function() {
  // Initialize any global components or functionality
  console.log('SuperCalc initialized');
  
  // Add event listeners for navigation if needed
  const navLinks = document.querySelectorAll('a.calculator-card');
  if (navLinks) {
    navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        // You can add transition effects or analytics tracking here
        console.log(`Navigating to: ${this.getAttribute('href')}`);
      });
    });
  }
});