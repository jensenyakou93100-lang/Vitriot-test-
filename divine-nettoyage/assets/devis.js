/* Divine Nettoyage — assistant de devis en 4 étapes.
   Les données partent vers FormSubmit (même adresse que l'ancien formulaire) une fois le site en ligne. */
(function () {
  document.body.classList.add('page-devis');
  var form = document.getElementById('devis');
  if (!form) return;
  var steps = Array.prototype.slice.call(form.querySelectorAll('.wz-step'));
  var cur = 1;
  var nEl = document.getElementById('wz-n');
  var labelEl = document.getElementById('wz-label');
  var fill = document.getElementById('wz-fill');
  var prev = document.getElementById('wz-prev');
  var next = document.getElementById('wz-next');
  var sumT = document.getElementById('sum-t');
  var sumS = document.getElementById('sum-s');
  var done = document.getElementById('wz-done');
  var foot = document.getElementById('wz-foot');
  var top = document.querySelector('.wz-top');
  var euro = function (n) { return n.toLocaleString('fr-FR') + ' €'; };

  // L'aperçu (hors du vrai site) ne peut pas envoyer de formulaire vers un autre domaine.
  var host = location.hostname || '';
  var isPreview = !host || /claude|anthropic|localhost|127\.0\.0\.1/.test(host) || location.protocol === 'file:';

  // ---------- quantités
  function items() {
    return Array.prototype.slice.call(form.querySelectorAll('.it')).map(function (it) {
      return {
        el: it, id: it.dataset.id, name: it.dataset.name,
        price: it.dataset.price ? Number(it.dataset.price) : null,
        qty: Number(it.querySelector('output').value || it.querySelector('output').textContent) || 0,
        cat: it.closest('.cat')
      };
    });
  }
  function setQty(it, q) {
    q = Math.max(0, Math.min(30, q));
    var out = it.querySelector('output');
    out.value = q; out.textContent = q;
    it.querySelector('.q-minus').disabled = q === 0;
    refresh();
  }
  form.querySelectorAll('.it').forEach(function (it) {
    it.querySelector('.q-minus').disabled = true;
    it.querySelector('.q-plus').addEventListener('click', function () { setQty(it, Number(it.querySelector('output').textContent) + 1); });
    it.querySelector('.q-minus').addEventListener('click', function () { setQty(it, Number(it.querySelector('output').textContent) - 1); });
  });

  // ---------- catégories dépliables
  function openCat(cat, open) {
    var b = cat.querySelector('.cat-h'), p = cat.querySelector('.cat-p');
    b.setAttribute('aria-expanded', open ? 'true' : 'false');
    p.hidden = !open;
  }
  form.querySelectorAll('.cat').forEach(function (cat) {
    cat.querySelector('.cat-h').addEventListener('click', function () {
      openCat(cat, this.getAttribute('aria-expanded') !== 'true');
    });
  });

  // pré-sélection depuis une page de prestation (devis.html#canape)
  var pre = { canape: 'canape', matelas: 'matelas', tapis: 'tapis', vitres: 'vitres', pro: 'commerce', veranda: 'veranda' }[(location.hash || '').slice(1)];
  if (pre) {
    var c = document.getElementById('c-' + pre);
    if (c) {
      openCat(c, true);
      if (pre === 'canape' || pre === 'matelas' || pre === 'tapis') setQty(c.querySelector('.it'), 1);
    }
  }

  function isPro() { var r = form.querySelector('input[name="Profil"]:checked'); return r && r.value === 'Professionnel'; }

  function summary() {
    var list = items().filter(function (i) { return i.qty > 0; });
    var count = list.reduce(function (s, i) { return s + i.qty; }, 0);
    var known = list.filter(function (i) { return i.price != null; });
    var base = known.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    var quote = list.some(function (i) { return i.price == null; });
    return { list: list, count: count, base: base, quote: quote };
  }

  function refresh() {
    var s = summary();
    form.querySelectorAll('.cat').forEach(function (cat) {
      var n = 0;
      cat.querySelectorAll('.it output').forEach(function (o) { n += Number(o.textContent) || 0; });
      var badge = cat.querySelector('.cat-n');
      badge.hidden = n === 0; badge.textContent = n;
      cat.classList.toggle('has', n > 0);
    });
    if (!s.count) {
      sumT.textContent = 'Aucun élément';
      sumS.textContent = "Ajoutez ce qu'il faut nettoyer";
    } else {
      sumT.textContent = s.count + (s.count > 1 ? ' éléments' : ' élément');
      if (s.base > 0) {
        var pay = isPro() ? s.base : s.base / 2;
        sumS.textContent = 'Dès ' + euro(pay) + (isPro() ? ' HT indicatif' : " après crédit d'impôt") + (s.quote ? ' + le reste sur devis' : '');
      } else {
        sumS.textContent = 'Prix ferme sous 24 h, sur devis';
      }
    }
    if (cur === 1) next.disabled = !s.count;
  }
  form.querySelectorAll('input[name="Profil"]').forEach(function (r) { r.addEventListener('change', refresh); });

  // ---------- photos : réduites avant l'envoi
  form.querySelectorAll('.ph-slot').forEach(function (slot) {
    var input = slot.querySelector('input'), img = slot.querySelector('img'), empty = slot.querySelector('.ph-empty'), del = slot.querySelector('.ph-del');
    function clear() { input.value = ''; img.hidden = true; img.removeAttribute('src'); empty.hidden = false; del.hidden = true; }
    del.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); clear(); });
    input.addEventListener('change', function () {
      var f = input.files && input.files[0];
      if (!f) return clear();
      var url = URL.createObjectURL(f);
      var im = new Image();
      im.onload = function () {
        img.src = url; img.hidden = false; empty.hidden = true; del.hidden = false;
        var max = 1600, w = im.naturalWidth, h = im.naturalHeight, k = Math.min(1, max / Math.max(w, h));
        if (k === 1 && f.size < 1.5e6) return;
        try {
          var cv = document.createElement('canvas'); cv.width = Math.round(w * k); cv.height = Math.round(h * k);
          cv.getContext('2d').drawImage(im, 0, 0, cv.width, cv.height);
          cv.toBlob(function (b) {
            if (!b || typeof DataTransfer === 'undefined') return;
            var dt = new DataTransfer();
            dt.items.add(new File([b], (f.name || 'photo').replace(/\.\w+$/, '') + '.jpg', { type: 'image/jpeg' }));
            input.files = dt.files;
          }, 'image/jpeg', 0.82);
        } catch (e) { /* on garde le fichier d'origine */ }
      };
      im.onerror = function () { clear(); };
      im.src = url;
    });
  });

  // ---------- navigation entre étapes
  function show(n) {
    cur = n;
    steps.forEach(function (s) { s.hidden = Number(s.dataset.step) !== n; });
    nEl.textContent = n;
    labelEl.textContent = steps[n - 1].dataset.label;
    fill.style.width = (n * 25) + '%';
    prev.hidden = n === 1;
    foot.classList.toggle('last', n === 4);
    next.textContent = n === 4 ? 'Envoyer ma demande' : 'Continuer';
    next.disabled = false;
    if (n === 4) buildRecap();
    refresh();
    var y = form.getBoundingClientRect().top + window.scrollY - 160;
    window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
    var h = steps[n - 1].querySelector('h1'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  }
  function err(id, on) { var e = document.getElementById(id); if (e) e.hidden = !on; }

  function validate(n) {
    if (n === 1) { var ok = summary().count > 0; err('err-1', !ok); return ok; }
    if (n === 2) {
      var cp = document.getElementById('f-cp');
      var ok2 = cp.value.trim().length >= 3;
      cp.classList.toggle('bad', !ok2); err('err-2', !ok2);
      if (!ok2) cp.focus();
      return ok2;
    }
    if (n === 4) {
      var nom = document.getElementById('f-nom'), tel = document.getElementById('f-tel');
      var okN = nom.value.trim().length >= 2;
      var okT = tel.value.replace(/\D/g, '').length >= 9;
      nom.classList.toggle('bad', !okN); tel.classList.toggle('bad', !okT);
      err('err-4', !(okN && okT));
      if (!okN) nom.focus(); else if (!okT) tel.focus();
      return okN && okT;
    }
    return true;
  }

  function buildRecap() {
    var s = summary();
    var r = document.getElementById('recap');
    var lines = s.list.map(function (i) {
      return '<li><span>' + i.qty + ' × ' + i.name + '</span><span>' + (i.price != null ? 'dès ' + euro(i.price * i.qty) : 'sur devis') + '</span></li>';
    }).join('');
    var where = document.getElementById('f-cp').value.trim();
    var freq = (form.querySelector('input[name="Frequence"]:checked') || {}).value;
    var tot = '';
    if (s.base > 0) {
      tot = isPro()
        ? '<div class="tot"><span>Base indicative<small>' + (s.quote ? 'hors éléments sur devis' : 'confirmée par Jensen') + '</small></span><span>dès ' + euro(s.base) + '</span></div>'
        : '<div class="tot"><span>Vous réglez<small>après crédit d\'impôt de 50 %' + (s.quote ? ', hors éléments sur devis' : '') + '</small></span><span>dès ' + euro(s.base / 2) + '</span></div>';
    }
    r.innerHTML = '<h3>Récapitulatif</h3><ul>' + lines + '</ul>' + tot +
      '<p style="color:var(--ink-2);font-size:.84rem">' + (isPro() ? 'Professionnel' : 'Particulier') + (where ? ' · ' + where.replace(/[<>&]/g, '') : '') + (freq ? ' · ' + freq : '') + '</p>';
  }

  prev.addEventListener('click', function () { if (cur > 1) show(cur - 1); });
  next.addEventListener('click', function () {
    if (!validate(cur)) return;
    if (cur < 4) return show(cur + 1);
    submit();
  });
  form.addEventListener('submit', function (e) { e.preventDefault(); next.click(); });
  form.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT' && e.target.type !== 'file') { e.preventDefault(); next.click(); }
  });

  function submit() {
    var s = summary();
    document.getElementById('f-presta').value = s.list.map(function (i) { return i.qty + ' × ' + i.name; }).join(' ; ');
    document.getElementById('f-estim').value = s.base > 0
      ? (isPro() ? 'Base indicative dès ' + euro(s.base) : 'Dès ' + euro(s.base / 2) + " après crédit d'impôt (" + euro(s.base) + ' avant)') + (s.quote ? ' + éléments sur devis' : '')
      : 'Sur devis';
    document.getElementById('f-next').value = location.origin + location.pathname + '?envoye=1';
    if (isPreview) {
      var m = document.getElementById('err-send');
      m.className = 'preview-note';
      m.textContent = "Aperçu : tout est prêt. L'envoi de la demande fonctionnera une fois le site en ligne sur divinenettoyage.fr.";
      m.hidden = false;
      return;
    }
    next.disabled = true;
    next.textContent = 'Envoi…';
    HTMLFormElement.prototype.submit.call(form);
  }

  // ---------- retour après envoi
  if (/[?&]envoye=1/.test(location.search)) {
    form.hidden = true; foot.hidden = true; if (top) top.hidden = true; done.hidden = false;
  }

  refresh();
})();
