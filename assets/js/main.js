const hamburger = document.getElementById('hamburgerBtn');
const sideMenu = document.getElementById('sideMenu');
const backdrop = document.getElementById('menuBackdrop');

if (hamburger && sideMenu && backdrop) {
  const background = document.querySelectorAll('header, main, footer, .skip-link');
  const setMenuOpen = (open, restoreFocus = true) => {
    sideMenu.classList.toggle('open', open);
    backdrop.classList.toggle('show', open);
    hamburger.classList.toggle('active', open);
    document.body.classList.toggle('menu-open', open);
    hamburger.setAttribute('aria-expanded', String(open));
    hamburger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    sideMenu.inert = !open;
    background.forEach((element) => { element.inert = open; });
    if (open) sideMenu.querySelector('a')?.focus();
    else if (restoreFocus) hamburger.focus();
  };

  hamburger.addEventListener('click', () => setMenuOpen(!sideMenu.classList.contains('open')));
  backdrop.addEventListener('click', () => setMenuOpen(false));
  sideMenu.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link) return;
    setMenuOpen(false);
    const url = new URL(link.href);
    if (url.pathname === location.pathname && url.hash) {
      const target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (target) {
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
      }
    }
  });
  document.addEventListener('keydown', (event) => {
    if (!sideMenu.classList.contains('open')) return;
    if (event.key === 'Escape') setMenuOpen(false);
    if (event.key === 'Tab') {
      const links = [...sideMenu.querySelectorAll('a[href]')];
      const items = [hamburger, ...links];
      const index = items.indexOf(document.activeElement);
      event.preventDefault();
      items[(index + (event.shiftKey ? -1 : 1) + items.length) % items.length].focus();
    }
  });
}

document.querySelectorAll('[data-year]').forEach((element) => {
  element.textContent = new Date().getFullYear();
});
