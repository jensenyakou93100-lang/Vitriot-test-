/* Divine Nettoyage — comportements communs à toutes les pages */
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  // En-tête : fond clair une fois la photo d'ouverture dépassée
  var header = document.querySelector('.site-header');
  var hero = document.querySelector('.hero');
  function onScroll() {
    if (!header) return;
    var limit = hero ? Math.max(80, hero.offsetHeight - 90) : 20;
    header.classList.toggle('scrolled', window.scrollY > limit);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Menu mobile
  var mnav = document.getElementById('mnav');
  var openBtn = document.querySelector('.hdr-right .burger');
  var closeBtn = mnav && mnav.querySelector('.burger');
  function setMenu(open) {
    if (!mnav) return;
    mnav.classList.toggle('open', open);
    if (openBtn) openBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    if (open && closeBtn) closeBtn.focus();
  }
  if (openBtn) openBtn.addEventListener('click', function () { setMenu(true); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setMenu(false); if (openBtn) openBtn.focus(); });
  if (mnav) mnav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { setMenu(false); closeDd(); } });

  // Menu déroulant « Prestations » (clic au doigt ou au clavier)
  var dd = document.querySelector('.dd');
  function closeDd() { if (dd) { dd.classList.remove('open'); dd.firstElementChild.setAttribute('aria-expanded', 'false'); } }
  if (dd) {
    dd.firstElementChild.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !dd.classList.contains('open');
      dd.classList.toggle('open', open);
      this.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function (e) { if (!dd.contains(e.target)) closeDd(); });
  }

  // Avis supplémentaires
  document.querySelectorAll('[data-more]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var box = document.getElementById(btn.getAttribute('data-more'));
      if (!box) return;
      var show = !box.classList.contains('show');
      box.classList.toggle('show', show);
      btn.setAttribute('aria-expanded', show ? 'true' : 'false');
      btn.textContent = show ? 'Masquer ces avis' : "Lire d'autres avis";
    });
  });

  // Apparition douce au défilement : le contenu reste visible si le script ne tourne pas,
  // et seuls les blocs encore sous la ligne de flottaison sont masqués puis révélés.
  var items = document.querySelectorAll('.reveal');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.remove('pending'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    var vh = window.innerHeight;
    items.forEach(function (el) {
      if (el.getBoundingClientRect().top > vh * 0.95) { el.classList.add('pending'); io.observe(el); }
    });
    // impression ou capture : tout afficher
    window.addEventListener('beforeprint', function () { items.forEach(function (el) { el.classList.remove('pending'); }); });
  }

  // Année du pied de page
  document.querySelectorAll('.yr').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
