# Génère le site Divine Nettoyage (pages statiques) dans le dossier donné en argument.
import json, os, sys, html

OUT = sys.argv[1]
ZONES = json.load(open(os.path.join(os.path.dirname(__file__), 'zones.json'), encoding='utf-8'))

TEL = "06 99 14 25 08"
TEL_HREF = "tel:+33699142508"
MAIL = "Divinetextile.pro@gmail.com"
GOOGLE = "https://share.google/4LWD04qh5UaOUdYKN"
IG = "https://www.instagram.com/divinenettoyage"
FB = "https://www.facebook.com/share/1EhrKePbFw/"
TT = "https://www.tiktok.com/@divinetextile"
SIRET = "989 702 543 00020"
SITE = "https://divinenettoyage.fr"

# ---------------------------------------------------------------- icônes
def ic(name):
    p = {
        'chev': '<path d="M9 6l6 6-6 6"/>',
        'down': '<path d="M6 9l6 6 6-6"/>',
        'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'ext': '<path d="M7 17L17 7M8 7h9v9"/>',
        'phone': '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>',
        'menu': '<path d="M4 8h16M4 16h16"/>',
        'close': '<path d="M6 6l12 12M18 6L6 18"/>',
        'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        'x': '<path d="M7 7l10 10M17 7L7 17"/>',
        'play': '<path d="M8 5.5v13l11-6.5z" fill="currentColor" stroke="none"/>',
        'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
        'doc': '<path d="M7 3h7l5 5v13H7zM14 3v5h5M10 13h6M10 17h6"/>',
        'spark': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
        'shield': '<path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
        'search': '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
        'drop': '<path d="M12 3s6 6.5 6 11a6 6 0 01-12 0c0-4.5 6-11 6-11z"/>',
        'brush': '<path d="M14 4l6 6-8 8H6v-6z"/><path d="M4 20l2-2"/>',
        'vac': '<path d="M4 20h9M8 20V9a5 5 0 0110 0v3"/><circle cx="18" cy="15" r="3"/>',
        'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
        'eye': '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        'pole': '<path d="M6 21L18 3M15 3h6v4"/>',
        'cal': '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
        'home': '<path d="M4 11l8-7 8 7v9H4z"/><path d="M10 20v-6h4v6"/>',
        'store': '<path d="M4 9l2-5h12l2 5M4 9v11h16V9M4 9h16"/><path d="M10 20v-5h4v5"/>',
        'build': '<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 12h6M9 16h6"/>',
        'bed': '<path d="M3 18V8M3 14h18v4M21 14v-2a3 3 0 00-3-3h-7v5"/><circle cx="7" cy="11" r="2"/>',
        'sofa': '<path d="M4 11V8a2 2 0 012-2h12a2 2 0 012 2v3"/><path d="M2 13a2 2 0 014 0v2h12v-2a2 2 0 014 0v5H2z"/><path d="M5 18v2M19 18v2"/>',
        'rug': '<rect x="5" y="4" width="14" height="16" rx="1"/><path d="M8 4V2M12 4V2M16 4V2M8 22v-2M12 22v-2M16 22v-2M9 9h6v6H9z"/>',
        'car': '<path d="M5 16V11l2-5h10l2 5v5M3 16h18v3H3z"/><circle cx="7.5" cy="16" r="1.5"/><circle cx="16.5" cy="16" r="1.5"/>',
        'win': '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M4 12h16"/>',
        'bay': '<rect x="3" y="4" width="18" height="17" rx="1"/><path d="M12 4v17M3 21h18"/>',
        'veranda': '<path d="M3 21V10l9-6 9 6v11M3 10h18M8 21v-9M16 21v-9"/>',
        'cam': '<path d="M4 8h3l2-3h6l2 3h3v12H4z"/><circle cx="12" cy="13.5" r="3.5"/>',
        'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'euro': '<path d="M17 6.5A7 7 0 007 12a7 7 0 0010 5.5M4 10h9M4 14h9"/>',
        'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
        'pin': '<path d="M12 21s7-6 7-11a7 7 0 00-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
        'leaf': '<path d="M5 19c0-9 6-14 15-14 0 9-5 15-14 15"/><path d="M5 19l7-7"/>',
    }[name]
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

LOGO = ('<svg viewBox="0 0 48 48" aria-hidden="true"><circle class="bg" cx="24" cy="24" r="23" fill="#3A2A1C"/>'
        '<path d="M24 10 L26.6 20.4 L37 23 L26.6 25.6 L24 36 L21.4 25.6 L11 23 L21.4 20.4 Z" fill="#C3982F"/>'
        '<circle cx="34" cy="14" r="1.8" fill="#E3C77A"/><circle cx="14" cy="33" r="1.3" fill="#E3C77A"/></svg>')

def brand(href="index.html"):
    return (f'<a class="brand" href="{href}" aria-label="Divine Nettoyage, accueil">{LOGO}'
            '<span class="brand-txt"><span class="brand-name">Divine Nettoyage</span>'
            '<span class="brand-sub">Vitres &amp; Textiles</span></span></a>')

SERVICES = [
    ('nettoyage-vitres.html', 'Nettoyage de vitres', 'Sur devis'),
    ('nettoyage-canape.html', 'Nettoyage de canapé', 'dès 80 €'),
    ('nettoyage-matelas.html', 'Nettoyage de matelas', 'dès 70 €'),
    ('nettoyage-tapis.html', 'Nettoyage de tapis', 'dès 50 €'),
]

# ---------------------------------------------------------------- gabarit
def header(current, light=False):
    svc_current = current in [s[0] for s in SERVICES]
    def cur(p): return ' aria-current="page"' if p == current else ''
    dd = ''.join(f'<a href="{h}"{cur(h)}>{n}<small>{p}</small></a>' for h, n, p in SERVICES)
    mdd = ''.join(f'<a class="sub" href="{h}">{n}<small>{p}</small></a>' for h, n, p in SERVICES)
    return f'''
<header class="site-header{' light' if light else ''}" id="top">
  <div class="bar">
    {brand()}
    <nav class="mainnav" aria-label="Navigation principale">
      <div class="dd{' current' if svc_current else ''}">
        <button type="button" aria-haspopup="true" aria-expanded="false">Prestations {ic('down')}</button>
        <div class="dd-menu">{dd}</div>
      </div>
      <a href="professionnels.html"{cur('professionnels.html')}>Pros</a>
      <a href="zones.html"{cur('zones.html')}>Zones</a>
      <a href="credit-impot.html"{cur('credit-impot.html')}>Crédit d'impôt</a>
      <a href="index.html#avis">Avis</a>
      <a href="index.html#contact">Contact</a>
    </nav>
    <div class="hdr-right">
      <a class="hdr-tel" href="{TEL_HREF}">{ic('phone')}{TEL}</a>
      <a class="btn btn-white hdr-cta" href="devis.html">Devis gratuit {ic('chev')}</a>
      <button class="burger" type="button" aria-label="Ouvrir le menu" aria-controls="mnav" aria-expanded="false">{ic('menu')}</button>
    </div>
  </div>
</header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="mnav-top">{brand()}<button class="burger" type="button" aria-label="Fermer le menu">{ic('close')}</button></div>
  <nav aria-label="Menu mobile">
    <a href="index.html">Accueil</a>
    {mdd}
    <a href="professionnels.html">Professionnels</a>
    <a href="zones.html">Zones d'intervention</a>
    <a href="credit-impot.html">Crédit d'impôt</a>
    <a href="index.html#avis">Avis clients</a>
  </nav>
  <div class="mnav-cta">
    <a class="btn btn-white" href="devis.html">Demander un devis gratuit</a>
    <a class="btn btn-ghost" href="{TEL_HREF}">{ic('phone')} {TEL}</a>
    <p>Joignable 7 jours sur 7 · Réponse sous 24 h</p>
  </div>
</div>'''

def footer():
    zl = ''.join(f'<li><a href="zones.html">{d}</a></li>' for d in ["Val-d'Oise (95)", "Paris (75)", "Hauts-de-Seine (92)", "Seine-Saint-Denis (93)", "Toute l'Île-de-France"])
    sv = ''.join(f'<li><a href="{h}">{n}</a></li>' for h, n, _ in SERVICES)
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <div class="fgrid">
      <div class="fbrand">
        {brand()}
        <p>Nettoyage de vitres et de textiles · Val-d'Oise<br>Particuliers et professionnels, dans toute l'Île-de-France.</p>
        <div class="contact"><a href="{TEL_HREF}">{TEL}</a><a href="mailto:{MAIL}">{MAIL}</a></div>
        <div class="fsoc"><a href="{IG}" target="_blank" rel="noopener">Instagram</a><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{TT}" target="_blank" rel="noopener">TikTok</a></div>
      </div>
      <div class="fcol"><h4>Prestations</h4><ul>{sv}<li><a href="professionnels.html">Pour les pros</a></li><li><a href="credit-impot.html">Crédit d'impôt 50 %</a></li></ul></div>
      <div class="fcol"><h4>Zones</h4><ul>{zl}</ul></div>
      <div class="fcol"><h4>Entreprise</h4><ul><li><a href="devis.html">Demander un devis</a></li><li><a href="{GOOGLE}" target="_blank" rel="noopener">Nos avis Google</a></li><li><span>SIRET {SIRET}</span></li><li><span>Assurée ORUS · RC Pro</span></li></ul></div>
    </div>
  </div>
  <div class="wrap"><div class="fbottom"><span>© <span class="yr">2026</span> Divine Nettoyage · Entreprise déclarée et assurée</span><span>Service à la personne · Crédit d'impôt 50 %</span></div></div>
</footer>'''

def page(fname, title, desc, body, current=None, light=False, extra_head='', jsonld=None, scripts=''):
    ld = ''
    if jsonld:
        ld = '\n'.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    url = SITE + '/' + ('' if fname == 'index.html' else fname)
    doc = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="FR-95">
<meta name="geo.placename" content="Val-d'Oise, Île-de-France">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Divine Nettoyage">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}/images/partage.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#120E0A">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="images/icon-192.png">
<link rel="apple-touch-icon" href="images/icon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Fraunces:opsz,wght@9..144,600&display=swap">
<link rel="stylesheet" href="assets/style.css">
{extra_head}
{ld}
</head>
<body>
{header(current or fname, light)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/site.js"></script>
{scripts}
</body>
</html>
'''
    key = {'nettoyage-canape.html': 'canape', 'nettoyage-matelas.html': 'matelas', 'nettoyage-tapis.html': 'tapis', 'nettoyage-vitres.html': 'vitres', 'professionnels.html': 'pro'}.get(fname)
    if key:
        doc = doc.replace('href="devis.html"', f'href="devis.html#{key}"')
    with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
        f.write(doc)
    print('écrit', fname, len(doc))

# ---------------------------------------------------------------- blocs réutilisables
def hero_page(img, crumb, tag, h1, lede, pos='50% 40%', cta_label='Demander un devis', cta_href='devis.html'):
    return f'''
<section class="hero page-hero">
  <div class="hero-media" style="--pos:{pos}"><img src="images/{img}" alt="" fetchpriority="high"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a><i>›</i><span aria-current="page">{crumb}</span></nav>
    <span class="pill-tag">{tag}</span>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="actions">
      <a class="btn btn-white" href="{cta_href}">{cta_label} {ic('arrow')}</a>
      <a class="btn btn-ghost" href="{TEL_HREF}">{ic('phone')} {TEL}</a>
    </div>
  </div>
</section>'''

def checks(items, cls=''):
    mark = ic('x') if 'x' in cls.split() else ic('check')
    return f'<ul class="checks {cls}">' + ''.join(f'<li>{mark}<span>{i}</span></li>' for i in items) + '</ul>'

def steps(items):
    out = ''
    for n, (icon, h, p) in enumerate(items, 1):
        out += f'<div class="step reveal"><div class="head"><span class="ic">{ic(icon)}</span><span class="mono">Étape {n}</span></div><h3>{h}</h3><p>{p}</p></div>'
    return f'<div class="steps">{out}</div>'

def faq(items, cat=None):
    out = ''
    for q, a in items:
        out += f'<details><summary>{q}</summary><p>{a}</p></details>'
    return out

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]}

def cta(title_html="Prêt à retrouver <span class=\"gold\">l'éclat</span>&nbsp;?", text="Devis gratuit sous 24 h. Crédit d'impôt de 50 % pour les particuliers. Intervention dans le Val-d'Oise et toute l'Île-de-France.", img='vitres-finition.jpg', anchor='contact'):
    return f'''
<section class="section" id="{anchor}">
  <div class="wrap">
    <div class="ctacard reveal">
      <img src="images/{img}" alt="" loading="lazy">
      <div class="l">
        <h2>{title_html}</h2>
        <p>{text}</p>
        <div class="actions">
          <a class="btn btn-white" href="devis.html">Demander un devis {ic('arrow')}</a>
          <a class="btn btn-ghost" href="{TEL_HREF}">{TEL}</a>
        </div>
      </div>
      <dl>
        <div><dt>Zone</dt><dd>Val-d'Oise et toute l'Île-de-France, jusqu'au sud de l'Oise</dd></div>
        <div><dt>Disponibilité</dt><dd>Joignable 7/7 · Interventions du lundi au samedi, créneaux en soirée possibles</dd></div>
        <div><dt>Téléphone</dt><dd><a href="{TEL_HREF}">{TEL}</a></dd></div>
        <div><dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
      </dl>
    </div>
  </div>
</section>'''

REVIEWS = [
    ("Une qualité incroyable.", "Prestation d'une qualité incroyable ! Merci à Jensen pour sa disponibilité et son travail rigoureux. Je vous recommande Divine Nettoyage les yeux fermés.", "Tiphanie Verbeeck"),
    ("Mes vitres sont impeccables.", "Très bonne prestation que je compte réitérer. Divine Nettoyage a été très professionnel et mes vitres sont impeccables, je recommande.", "Julie Duhourcau"),
    ("Comme au premier jour.", "Merci pour son aide, c'était parfait ! Jensen est professionnel et méticuleux. Je suis heureuse de retrouver mon canapé comme au premier jour.", "Noémie Sierra"),
    ("Un travail remarquable.", "Jensen a fait preuve d'un grand professionnalisme lors de son intervention ce matin. Il a nettoyé mon canapé ainsi que mon matelas avec beaucoup de soin et d'efficacité. Je recommande ses services à 100 %.", "Sonia Bouayad"),
    ("Un résultat comme neuf.", "J'ai fait appel à Divine Nettoyage pour le nettoyage de matelas, un résultat comme neuf. Merci pour cette prestation de qualité et super rapide.", "Romain Recchia"),
    ("De confiance et chaleureux.", "Nettoyage impeccable après 2 ans sans avoir nettoyé mes vitres, Jensen est de confiance et chaleureux. Je recommande vivement et referai appel à vos services cet été !", "Axel"),
    ("Très qualitatif.", "Nettoyage de mon tapis et canapé très qualitatif, Jensen est très sympathique et explique bien le processus de nettoyage. Je recommande fortement.", "Pablo Michaud"),
    ("Sérieux et soigné.", "Jensen a été très professionnel et efficace du début à la fin. Travail sérieux, soigné et de qualité. C'est une personne de confiance que je recommande vivement pour son sérieux.", "Marion Amelin"),
    ("Le résultat est top.", "Je suis très contente du résultat. Intervention très professionnelle, personne agréable, ponctuelle et efficace. Il a pris le temps d'expliquer le nettoyage et le résultat sur mon canapé est top.", "Mélissa Condo"),
]

def quotes(rs):
    return ''.join(f'<figure class="quote reveal" style="margin:0"><h3>« {t} »</h3><p>{p}</p><figcaption class="who"><b>{w}</b> · Avis Google</figcaption></figure>' for t, p, w in rs)

def reviews_block(sel=(0, 1, 2), more=True, title=None):
    first = [REVIEWS[i] for i in sel]
    rest = [r for i, r in enumerate(REVIEWS) if i not in sel]
    more_html = f'<div class="quotes more-quotes" id="more-quotes">{quotes(rest)}</div>' if more else ''
    btn = '<button class="btn btn-line" type="button" data-more="more-quotes" aria-expanded="false">Lire d\'autres avis</button>' if more else ''
    head = f'<div class="shead center"><span class="eyebrow">Avis clients</span><h2>{title}</h2></div>' if title else ''
    return f'''
<section class="section" id="avis">
  <div class="wrap">
    {head}
    <div class="rating-line"><span class="stars" aria-hidden="true">★★★★★</span><span class="mono">5,0/5 sur Google · 43 avis</span></div>
    <div class="quotes">{quotes(first)}</div>
    {more_html}
    <div class="quotes-actions">{btn}<a class="btn btn-dark" href="{GOOGLE}" target="_blank" rel="noopener">Voir les 43 avis sur Google {ic('arrow')}</a></div>
  </div>
</section>'''

def zones_dark(title='Le Val-d\'Oise et <span class="gold">toute l\'Île-de-France.</span>', text="Du Val-d'Oise à Paris, en passant par les huit départements franciliens et le sud de l'Oise. Le déplacement est compris dans le prix annoncé."):
    deps = ["Val-d'Oise (95)", "Paris (75)", "Hauts-de-Seine (92)", "Seine-Saint-Denis (93)", "Val-de-Marne (94)", "Yvelines (78)", "Essonne (91)", "Seine-et-Marne (77)"]
    items = ''.join(f'<a href="zones.html#d{d[-3:-1]}">{d}</a>' for d in deps)
    return f'''
<section class="section dark">
  <div class="wrap">
    <div class="shead center"><span class="eyebrow">Zones d'intervention</span><h2>{title}</h2><p>{text}</p></div>
    <div class="zgrid">{items}</div>
    <p class="center-link"><a href="zones.html">Toutes les communes desservies {ic('ext')}</a></p>
  </div>
</section>'''

def trust():
    return f'''
<section class="section tight trust">
  <div class="wrap">
    <p class="mono" style="text-align:center;color:var(--ink-3);margin-bottom:36px">Ils nous font confiance</p>
    <div class="trust-row">
      <div class="trust-item"><b>5,0 ★</b><span class="mono">43 avis Google</span></div>
      <div class="trust-item"><b>7/7</b><span class="mono">Joignable tous les jours</span></div>
      <div class="trust-item"><b>ORUS</b><span class="mono">Assurance RC Pro</span></div>
      <div class="trust-item"><b>Urssaf</b><span class="mono">Avance immédiate · Unipros</span></div>
    </div>
    <p class="trust-note">Maisons, appartements, commerces et hôtellerie : Divine Nettoyage intervient chez des clients exigeants dans tout le Val-d'Oise et l'Île-de-France.</p>
  </div>
</section>'''

def taxcard(example="Exemple : canapé deux places", before="160 €", after="80 €", anchor='credit'):
    return f'''
<section class="section" id="{anchor}">
  <div class="wrap">
    <div class="taxcard reveal">
      <div class="l">
        <span class="mono">Service à la personne · Avance immédiate Urssaf</span>
        <h2>Vous ne payez que <span class="gold">la moitié</span>.</h2>
        <p>Le nettoyage à domicile ouvre droit au crédit d'impôt de 50 %. Avec l'avance immédiate, seule la moitié vous est prélevée à la facture. Vous n'avancez rien, et vous n'avez rien à déclarer ensuite.</p>
        <a class="link-arrow" href="credit-impot.html">Comprendre le crédit d'impôt {ic('chev')}</a>
      </div>
      <div class="r">
        <span class="mono">{example}</span>
        <div class="bigprice"><s>{before}</s><b>{after}</b></div>
        <p>Après crédit d'impôt de 50 %, via notre partenaire la coopérative Unipros. Avec l'avance immédiate, seuls {after} vous sont prélevés à la facture.</p>
      </div>
    </div>
  </div>
</section>'''

def pricecard(h, p, label, before, after, note):
    return f'''
<section class="section tight">
  <div class="wrap">
    <div class="pricecard reveal">
      <div class="l"><span class="eyebrow">Tarif</span><h2>{h}</h2><p>{p}</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:6px"><a class="btn btn-dark" href="devis.html">Obtenir mon prix {ic('arrow')}</a></div></div>
      <div class="r"><span class="mono">{label}</span><div class="bigprice"><s>{before}</s><b>{after}</b></div><p>{note}</p></div>
    </div>
  </div>
</section>'''

def honest(h, intro, items, note):
    lis = ''.join(f'<li><span>{i}</span></li>' for i in items)
    return f'''
<section class="section band">
  <div class="wrap honest">
    <div class="shead small" style="margin:0;align-content:start"><span class="eyebrow">En toute franchise</span><h2>{h}</h2><p>{intro}</p></div>
    <div><ol>{lis}</ol><p class="note">{note}</p></div>
  </div>
</section>'''

def tiles(items, cols=3):
    out = ''
    for icon, h, p in items:
        out += f'<div class="tile reveal"><span class="ic">{ic(icon)}</span><h3>{h}</h3><p>{p}</p></div>'
    cls = 'tiles four' if cols == 4 else 'tiles'
    return f'<div class="{cls}">{out}</div>'

def faq_section(items, title="Vos questions"):
    return f'''
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">FAQ</span><h2>{title}</h2></div>
    <div class="faq">{faq(items)}</div>
  </div>
</section>'''

def see_also(cur):
    links = [f'<a class="btn btn-line btn-sm" href="{h}">{n}</a>' for h, n, _ in SERVICES if h != cur]
    return f'<div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:28px">{"".join(links)}</div>'

BUSINESS = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": SITE + "/#entreprise",
    "name": "Divine Nettoyage",
    "description": "Nettoyage de textiles d'ameublement (canapés, matelas, tapis, sièges de voiture) par injection-extraction et lavage de vitres, à domicile et pour les professionnels, en Val-d'Oise et dans toute l'Île-de-France.",
    "url": SITE + "/", "email": MAIL, "telephone": "+33699142508", "image": SITE + "/images/partage.jpg",
    "logo": SITE + "/images/icon-512.png", "priceRange": "€€", "currenciesAccepted": "EUR",
    "paymentAccepted": "Carte bancaire, virement, espèces",
    "address": {"@type": "PostalAddress", "addressRegion": "Île-de-France", "addressCountry": "FR"},
    "areaServed": [{"@type": "AdministrativeArea", "name": d} for d in ZONES.keys()],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "43"},
    "sameAs": [IG, FB, TT],
}

def service_ld(name, desc, url, price):
    o = {"@context": "https://schema.org", "@type": "Service", "serviceType": name, "name": name, "description": desc,
         "url": SITE + "/" + url, "provider": {"@id": SITE + "/#entreprise"},
         "areaServed": [{"@type": "AdministrativeArea", "name": "Val-d'Oise (95)"}, {"@type": "AdministrativeArea", "name": "Île-de-France"}]}
    if price:
        o["offers"] = {"@type": "Offer", "priceCurrency": "EUR", "price": price, "description": f"À partir de {price} € après crédit d'impôt de 50 %"}
    return o

# ================================================================= ACCUEIL
home = f'''
<section class="hero">
  <div class="hero-media" style="--pos:55% 30%">
    <picture>
      <source media="(max-width: 600px)" srcset="images/jensen-portrait.jpg">
      <img src="images/hero-baie.jpg" alt="Jensen, fondateur de Divine Nettoyage, lave une baie vitrée à la raclette" fetchpriority="high">
    </picture>
  </div>
  <div class="wrap">
    <h1>Vitres impeccables, <span class="gold">canapés</span> comme neufs.</h1>
    <p class="lede">Nettoyage de vitres, de canapés, de matelas et de tapis à domicile. Crédit d'impôt de 50 % pour les particuliers, dans le Val-d'Oise et toute l'Île-de-France.</p>
    <div class="actions">
      <a class="btn btn-white" href="devis.html">Devis gratuit</a>
      <a class="btn btn-ghost" href="{TEL_HREF}">{ic('phone')} {TEL}</a>
    </div>
    <div class="hero-meta"><span><span class="stars" aria-hidden="true">★★★★★</span> 5,0 sur 43 avis Google</span><span>Réponse sous 24 h</span><span>Entreprise assurée</span></div>
  </div>
</section>

<section class="section" id="particuliers">
  <div class="wrap">
    <div class="shead center"><span class="eyebrow">Vitres &amp; textiles</span><h2>Chez vous ou<br>dans vos locaux.</h2>
      <p>Deux métiers faits avec le même soin : le verre et le tissu. Du matériel professionnel, un devis ferme sous 24 h et un seul interlocuteur, Jensen.</p></div>
    <div class="duo">
      <a class="pcard reveal" href="devis.html">
        <img src="images/canape-velours.jpg" alt="Canapé d'angle en velours côtelé après nettoyage" loading="lazy">
        <div class="in"><span class="mono">Particuliers</span><h3>Chez vous.</h3>
          <p>Canapé, matelas, tapis, sièges de voiture et vitres de votre maison ou de votre appartement. Ponctuel ou régulier.</p>
          <span class="price-chip">À partir de 50 €*</span><span class="fine">*après crédit d'impôt de 50 %</span></div>
        <div class="foot"><span>Devis gratuit</span>{ic('chev')}</div>
      </a>
      <a class="pcard reveal" href="professionnels.html" id="professionnels">
        <img src="images/vitrine.jpg" alt="Nettoyage de la vitrine d'un commerce" loading="lazy" style="object-position:50% 100%">
        <div class="in"><span class="mono">Professionnels</span><h3>Dans vos locaux.</h3>
          <p>Vitrines, bureaux, restaurants, hôtels et locations meublées. Passages planifiés hors horaires d'ouverture, même interlocuteur.</p></div>
        <div class="foot"><span>Découvrir l'offre pro</span>{ic('chev')}</div>
      </a>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Nos prestations</span><h2>Quatre prestations,<br>un même niveau d'exigence.</h2></div>
    <div class="services4">
      <a class="scard reveal" href="nettoyage-vitres.html"><div class="ph"><img src="images/vitres-hauteur.jpg" alt="Lavage de vitres en hauteur à la perche à eau pure" loading="lazy"></div>
        <div class="tx"><h3>Vitres</h3><p>Fenêtres, baies, vérandas, abris de piscine et vitrines. Eau pure et raclette.</p>
        <div class="row"><span class="from">Sur devis<small>formules d'entretien</small></span><span class="go">{ic('chev')}</span></div></div></a>
      <a class="scard reveal" href="nettoyage-canape.html"><div class="ph"><img src="images/canape-injection.jpg" alt="Nettoyage d'un canapé par injection-extraction" loading="lazy"></div>
        <div class="tx"><h3>Canapé</h3><p>Tissu, velours, microfibre. Taches, odeurs et poils d'animaux.</p>
        <div class="row"><span class="from">dès 80 €<small>au lieu de 160 €</small></span><span class="go">{ic('chev')}</span></div></div></a>
      <a class="scard reveal" href="nettoyage-matelas.html"><div class="ph"><img src="images/avant-apres-matelas.jpg" alt="Matelas taché avant et après nettoyage" loading="lazy" style="object-position:70% 50%"></div>
        <div class="tx"><h3>Matelas</h3><p>Auréoles, transpiration, acariens. Désinfection comprise.</p>
        <div class="row"><span class="from">dès 70 €<small>au lieu de 140 €</small></span><span class="go">{ic('chev')}</span></div></div></a>
      <a class="scard reveal" href="nettoyage-tapis.html"><div class="ph"><img src="images/canape-modulable.jpg" alt="Canapé modulable et tapis clair après nettoyage" loading="lazy"></div>
        <div class="tx"><h3>Tapis</h3><p>Laine, synthétique, moquettes. Les couleurs d'origine ressortent.</p>
        <div class="row"><span class="from">dès 50 €<small>au lieu de 100 €</small></span><span class="go">{ic('chev')}</span></div></div></a>
    </div>
  </div>
</section>

{taxcard()}

<section class="strip" aria-label="Nos interventions en images">
  <figure><img src="images/vitres-hauteur.jpg" alt="Lavage de vitres en hauteur à la perche télescopique" loading="lazy"><figcaption><span class="mono">Vitres</span>Perche à eau pure, jusqu'au 2e étage</figcaption></figure>
  <figure><img src="images/canape-angle-injection.jpg" alt="Jensen nettoie un canapé d'angle à l'injection-extraction" loading="lazy">
    <a class="play" href="{TT}" target="_blank" rel="noopener"><span class="disc">{ic('play')}</span><span>Voir nos vidéos</span></a></figure>
  <figure><img src="images/abri-piscine.jpg" alt="Nettoyage des vitres d'un abri de piscine" loading="lazy"><figcaption><span class="mono">Vérandas</span>Abri de piscine vitré</figcaption></figure>
</section>

{zones_dark()}
{trust()}
{reviews_block()}
{cta()}
'''
page('index.html', "Nettoyage canapé, tapis et vitres dès 50 € — Val-d'Oise (95) | Divine Nettoyage",
     "Nettoyage de canapé, matelas et tapis à domicile dès 50 € après crédit d'impôt, et lavage de vitres. Val-d'Oise et Île-de-France. Devis sous 24 h.",
     home, current='index.html', jsonld=[BUSINESS])

# ================================================================= VITRES
vit_faq = [
    ("Combien coûte un nettoyage de vitres ?", "Le tarif dépend du nombre de vitrages, de leur accessibilité et de leur état. Un devis gratuit est établi après un bref échange, avec photos ou dimensions. Nos formules d'entretien offrent 25 € dès 150 € de chantier, 50 € dès 200 € et 100 € dès 300 €."),
    ("Intervenez-vous sur les vitres en hauteur ?", "Oui. Nous utilisons une perche télescopique alimentée en eau pure, qui permet de laver jusqu'au deuxième étage depuis le sol, sans échelle ni nacelle. C'est plus sûr, plus rapide, et sans trace au séchage."),
    ("Qu'est-ce que l'eau pure ?", "C'est une eau débarrassée de son calcaire et de ses minéraux par filtration. Comme elle ne contient plus rien, elle sèche sans laisser la moindre marque : aucun essuyage n'est nécessaire après le rinçage."),
    ("Nettoyez-vous les vérandas et les abris de piscine ?", "Oui, c'est l'une de nos spécialités. Toits de véranda, verrières, abris de piscine vitrés, garde-corps en verre : ces surfaces s'encrassent vite et se nettoient rarement bien seules."),
    ("Faut-il être présent pendant l'intervention ?", "Pour l'extérieur, non, à condition que les accès soient disponibles. Pour l'intérieur, une présence est nécessaire à l'ouverture et pour le contrôle final. Chez les professionnels, nous pouvons intervenir avant l'ouverture ou après la fermeture."),
    ("Que se passe-t-il s'il pleut le jour prévu ?", "Une pluie fine n'empêche pas de travailler et ne salit pas une vitre correctement lavée. En cas de fortes intempéries, nous vous proposons de reporter sans frais."),
    ("Le nettoyage de vitres ouvre-t-il droit au crédit d'impôt ?", "Oui, pour les particuliers. Le lavage de vitres à domicile relève des services à la personne : 50 % du montant vous est rendu. Avec l'avance immédiate de l'Urssaf, vous ne réglez directement que la moitié."),
]
vitres = hero_page('vitres-finition.jpg', 'Nettoyage de vitres', 'Vitres', 'Nettoyage de vitres.',
    "Fenêtres, baies vitrées, vérandas, abris de piscine et vitrines lavés à l'eau pure et finis à la raclette. Sans trace, sans produit agressif, pour les particuliers comme pour les commerces.", pos='60% 30%') + f'''
<section class="section">
  <div class="wrap"><div class="lead-block reveal"><span class="eyebrow">Méthode</span><h2>Notre approche</h2>
    <p>Eau pure filtrée pour la hauteur, raclette et microfibre pour la finition, contrôle en contre-jour avant de partir. Nous lavons jusqu'au deuxième étage depuis le sol avec une perche télescopique : sans échelle, sans nacelle, sans risque pour votre façade.</p></div></div>
</section>
<section class="section band">
  <div class="wrap"><div class="shead small"><span class="eyebrow">Surfaces traitées</span><h2>Ce qu'on nettoie</h2></div>
  {checks(["Fenêtres et baies vitrées, intérieur et extérieur", "Vérandas, verrières et toitures vitrées", "Abris de piscine et parois vitrées de jardin", "Vitrines de commerce et façades d'enseigne", "Garde-corps et balustrades en verre", "Miroirs et parois de douche", "Volets, persiennes et stores extérieurs", "Rails, feuillures et appuis de fenêtre", "Vitres de bureaux et parties communes", "Vitrages après travaux ou fin de chantier"])}</div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="stack">
      <div class="reveal"><h2>Pourquoi un nettoyage de vitres professionnel&nbsp;?</h2>
        <p>La trace sur une vitre vient rarement du produit : elle vient du geste, de l'ordre des passages et de la finition des bords. Nous dépoussiérons avant de mouiller, raclons en un geste continu puis reprenons les quatre bords à la microfibre.</p>
        <p>En hauteur, l'eau pure ne contient plus ni calcaire ni minéraux : elle sèche sans la moindre marque. Chaque vitrage est contrôlé en contre-jour avant de passer au suivant.</p></div>
      <div class="reveal"><h2>Et pour les pros&nbsp;?</h2>
        <p>Commerces, bureaux, restaurants, halls d'immeuble : passages ponctuels ou contrat d'entretien, avant l'ouverture ou après la fermeture. Même méthode, même interlocuteur, facturation mensuelle sur contrat.</p>
        <p style="margin-top:16px"><a class="link-arrow" href="professionnels.html">Voir l'offre professionnelle {ic('chev')}</a></p></div>
    </div>
    <div class="reveal"><h2>Crédit d'impôt 50&nbsp;% pour les particuliers</h2>
      <p>Le lavage de vitres à domicile relève des services à la personne. Nous travaillons avec la coopérative Unipros : avec l'avance immédiate de l'Urssaf, vous ne réglez que la moitié du prix au moment de la facture, sans rien avancer et sans rien déclarer ensuite.</p>
      <p style="margin-top:16px"><a class="link-arrow" href="credit-impot.html">Comprendre le crédit d'impôt {ic('chev')}</a></p></div>
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Encadrements et rails</span><h2>Le verre, c'est la partie facile.</h2>
      <p>La saleté se loge dans les rails, les angles et les joints. C'est ce qu'on voit en ouvrant la fenêtre, et c'est souvent là que le nettoyage s'arrête. Pas chez nous.</p></div>
    <div class="rails reveal">
      <figure><img src="images/rail-avant.jpg" alt="Rail de baie vitrée encrassé avant nettoyage" loading="lazy"><span>Avant</span></figure>
      <figure><img src="images/rail-apres.jpg" alt="Le même rail après nettoyage" loading="lazy"><span>Après</span></figure>
      {checks(["Rails et glissières aspirés puis dégraissés", "Angles et recoins repris à la main", "Joints, montants et parcloses essuyés", "Poignées, charnières et appuis de fenêtre"], 'one')}
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Process</span><h2>De votre appel à la satisfaction.</h2></div>
    {steps([('chat', 'Votre demande', "Formulaire en 2 minutes ou appel direct. Quelques photos suffisent pour comprendre vos vitrages et l'accès."),
            ('doc', 'Devis sous 24 h', "Prix ferme et détaillé, crédit d'impôt de 50 % déjà calculé pour les particuliers."),
            ('spark', 'Intervention', "Jensen se déplace personnellement. Protection du sol, eau pure, raclette et microfibre."),
            ('shield', 'Contrôle en contre-jour', "Vérification vitre par vitre avec vous avant de partir. Une trace oubliée est reprise sur place.")])}
  </div>
</section>
<section class="section tight band">
  <div class="wrap compare">
    <div class="reveal"><h3><span class="eyebrow">Avec Divine Nettoyage</span></h3>{checks(["Vitres réellement transparentes, même en contre-jour", "Encadrements, rails et appuis compris", "Eau pure, sans produit agressif", "Crédit d'impôt de 50 % pour les particuliers"])}</div>
    <div class="reveal"><h3><span class="mono" style="color:var(--ink-3)">Sans entretien</span></h3>{checks(["Traces et voiles visibles à la lumière", "Calcaire incrusté sur les vitres", "Rails encrassés et encadrements oubliés", "Échelle et prise de risque en hauteur"], 'x')}</div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Sur le terrain</span><h2>Nos chantiers en images</h2></div>
    <div class="gallery">
      <figure class="reveal"><img src="images/vitres-hauteur.jpg" alt="Lavage de vitres en hauteur à la perche à eau pure" loading="lazy"><figcaption><span class="mono">Chez vous</span>Vitres en hauteur, perche à eau pure</figcaption></figure>
      <figure class="reveal"><img src="images/hero-baie.jpg" alt="Finition d'une baie vitrée à la raclette" loading="lazy"><figcaption><span class="mono">Chez vous</span>Baie vitrée, finition raclette</figcaption></figure>
      <figure class="reveal"><img src="images/abri-piscine.jpg" alt="Abri de piscine vitré" loading="lazy"><figcaption><span class="mono">Chez vous</span>Véranda et abri de piscine</figcaption></figure>
      <figure class="reveal"><img src="images/vitrine.jpg" alt="Vitrine de magasin" loading="lazy"><figcaption><span class="mono">Commerces</span>Vitrine de magasin</figcaption></figure>
      <figure class="reveal"><img src="images/vitres-exterieur.jpg" alt="Baie vitrée côté extérieur" loading="lazy"><figcaption><span class="mono">Chez vous</span>Baie vitrée, côté extérieur</figcaption></figure>
      <figure class="reveal"><img src="images/vitres-interieur.jpg" alt="Fenêtre côté intérieur" loading="lazy"><figcaption><span class="mono">Chez vous</span>Fenêtre, côté intérieur</figcaption></figure>
    </div>
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Formules d'entretien</span><h2>Une remise à chaque passage.</h2>
      <p>Trois rythmes de passage, chez vous comme dans votre commerce. À chaque intervention, un montant vous est offert dès que le chantier dépasse un seuil. Le nettoyage ponctuel et la fin de chantier sont chiffrés sur devis.</p></div>
    <div class="plans">
      <div class="plan reveal"><span class="mono">Vitres · Essentiel</span><div class="amt">25 €</div><p class="cond">offerts à chaque nettoyage, pour tout chantier de plus de 150 €</p>
        <ul><li>{ic('check')}2 passages par an</li><li>{ic('check')}Vitres intérieur et extérieur</li><li>{ic('check')}Encadrements, rails et appuis inclus</li></ul><a class="btn btn-line" href="devis.html">Choisir Essentiel</a></div>
      <div class="plan hot reveal"><span class="mono">Vitres · Confort</span><div class="amt">50 €</div><p class="cond">offerts à chaque nettoyage, pour tout chantier de plus de 200 €</p>
        <ul><li>{ic('check')}3 à 4 passages par an</li><li>{ic('check')}Vitres intérieur et extérieur</li><li>{ic('check')}Priorité sur le choix du créneau</li></ul><a class="btn btn-white" href="devis.html">Choisir Confort</a></div>
      <div class="plan reveal"><span class="mono">Vitres · Excellence</span><div class="amt">100 €</div><p class="cond">offerts à chaque nettoyage, pour tout chantier de plus de 300 €</p>
        <ul><li>{ic('check')}1 passage par mois</li><li>{ic('check')}Vitres, encadrements et volets</li><li>{ic('check')}Créneau réservé à l'année</li></ul><a class="btn btn-line" href="devis.html">Choisir Excellence</a></div>
    </div>
  </div>
</section>
{reviews_block(sel=(1, 5, 0), more=False, title="Ce que disent nos clients.")}
{faq_section(vit_faq)}
{cta(title_html="Devis gratuit pour <span class=\"gold\">vos vitres</span>.", text="Envoyez-nous deux ou trois photos de vos surfaces vitrées : nous vous répondons sous 24 heures avec un prix ferme, sans engagement.", img='vitres-hauteur.jpg')}
'''
page('nettoyage-vitres.html', "Laveur de vitres Val-d'Oise (95) — 50 % crédit d'impôt | Divine Nettoyage",
     "Nettoyage de vitres, baies vitrées, vérandas et vitrines à l'eau pure dans le Val-d'Oise et en Île-de-France. Crédit d'impôt 50 %, devis gratuit sous 24 h.",
     vitres, jsonld=[BUSINESS, service_ld("Nettoyage de vitres", "Nettoyage de vitres à l'eau pure et à la raclette, particuliers et professionnels, Val-d'Oise et Île-de-France.", 'nettoyage-vitres.html', None), faq_ld(vit_faq)])

# ================================================================= TEXTILES (canapé, matelas, tapis)
def textile_page(fname, crumb, tag, h1, lede, hero_img, pos, approach, what_h, what_items, steps_items, price, honest_data, extra, faq_items, gallery_html, ld_name, ld_desc, title, desc, cta_t):
    body = hero_page(hero_img, crumb, tag, h1, lede, pos=pos) + f'''
<section class="section">
  <div class="wrap"><div class="lead-block reveal"><span class="eyebrow">Méthode</span><h2>Notre approche</h2><p>{approach}</p></div></div>
</section>
<section class="section band">
  <div class="wrap"><div class="shead small"><span class="eyebrow">Ce qui disparaît</span><h2>{what_h}</h2></div>
  {tiles(what_items, 4)}</div>
</section>
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Process</span><h2>En quatre étapes.</h2></div>
    {steps(steps_items)}
  </div>
</section>
{pricecard(*price)}
{gallery_html}
{extra}
{honest(*honest_data)}
<section class="section tight">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Zone d'intervention</span><h2 style="margin-top:14px">Où j'interviens</h2>
      <p>Je me déplace dans tout le Val-d'Oise, en Île-de-France et dans le sud de l'Oise. Le déplacement est compris dans le prix annoncé.</p>
      <p>Taverny, Franconville, Ermont, Beauchamp, Saint-Leu-la-Forêt, Montmorency, Eaubonne, Domont, Sarcelles, Argenteuil, Cergy, Pontoise, Saint-Ouen-l'Aumône, L'Isle-Adam, Beaumont-sur-Oise, Persan, Chantilly et les communes alentour.</p>
      <p style="margin-top:16px"><a class="link-arrow" href="zones.html">Toutes les communes {ic('chev')}</a></p></div>
    <div class="reveal"><span class="eyebrow">Voir aussi</span><h2 style="margin-top:14px">Nos autres prestations</h2>
      <p>Le même soin pour vos vitres et vos autres textiles, le même jour si vous le souhaitez.</p>{see_also(fname)}</div>
  </div>
</section>
{faq_section(faq_items, "Ce qu'on nous demande le plus")}
{cta(title_html=cta_t, text="Envoyez une ou deux photos et les dimensions : Jensen vous répond sous 24 heures avec un prix ferme. Gratuit et sans engagement.", img='canape-injection.jpg')}
'''
    page(fname, title, desc, body, jsonld=[BUSINESS, service_ld(ld_name, ld_desc, fname, price[4].replace(' €', '')), faq_ld(faq_items)])

credit_q = ("Comment fonctionne le crédit d'impôt ?", "Vous réglez la facture, puis 50 % vous sont rendus par l'État au titre des services à la personne. Avec l'avance immédiate, la réduction est appliquée tout de suite : vous ne sortez que la moitié.")

# --- canapé
canape_gallery = f'''
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Avant / après</span><h2>La différence se voit.</h2></div>
    <div class="ba">
      <figure class="reveal"><img src="images/avant-apres-canape.jpg" alt="Canapé en velours côtelé avant et après nettoyage" loading="lazy"><figcaption>Canapé velours côtelé<span class="mono">Avant / Après</span></figcaption></figure>
      <figure class="reveal"><img src="images/canape-velours.jpg" alt="Canapé d'angle en velours côtelé après nettoyage" loading="lazy" style="aspect-ratio:1200/773;object-fit:cover;width:100%"><figcaption>Canapé d'angle velours<span class="mono">Après</span></figcaption></figure>
    </div>
    <div class="gallery" style="margin-top:16px">
      <figure class="reveal"><img src="images/canape-bleu.jpg" alt="Canapé d'angle bleu nettoyé par injection-extraction" loading="lazy"><figcaption><span class="mono">Particulier</span>Canapé d'angle bleu</figcaption></figure>
      <figure class="reveal"><img src="images/canape-creme.jpg" alt="Canapé d'angle crème remis à neuf" loading="lazy"><figcaption><span class="mono">Particulier</span>Canapé d'angle crème</figcaption></figure>
      <figure class="reveal"><img src="images/canape-modulable.jpg" alt="Grand canapé modulable clair après nettoyage" loading="lazy"><figcaption><span class="mono">Particulier</span>Canapé modulable clair</figcaption></figure>
    </div>
  </div>
</section>'''
canape_extra = f'''
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Les matières</span><h2>Les tissus que je traite.</h2><p>Chaque tissu réagit différemment. C'est la raison du test de couleur avant toute chose.</p></div>
    <div class="tiles">
      <div class="tile reveal"><h3>Velours et velours côtelé</h3><p>Les plus fréquents, et les plus spectaculaires une fois nettoyés. L'extraction redresse la fibre et la couleur revient. Séchage un peu plus long.</p></div>
      <div class="tile reveal"><h3>Microfibre et polyester</h3><p>Les tissus les plus tolérants. Les taches partent bien, le séchage est rapide, le résultat est très fiable.</p></div>
      <div class="tile reveal"><h3>Lin et coton</h3><p>Matières naturelles, sensibles au rétrécissement et aux auréoles. Je travaille à pression réduite et je sèche de façon homogène.</p></div>
      <div class="tile reveal"><h3>Chenille et tissus bouclés</h3><p>La saleté se loge entre les boucles. Le brossage mécanisé est indispensable, l'aspiration seule ne suffit jamais.</p></div>
      <div class="tile reveal"><h3>Alcantara et suédine</h3><p>Traitement délicat, produit spécifique, pression basse. Possible, mais je préviens toujours du résultat attendu avant de commencer.</p></div>
      <div class="tile reveal"><h3>Cuir et simili</h3><p>Ces matières ne se nettoient pas par injection-extraction. Je ne les traite pas, et je vous le dis franchement plutôt que de prendre le risque.</p></div>
    </div>
  </div>
</section>'''
textile_page('nettoyage-canape.html', 'Nettoyage de canapé', 'Canapé', 'Nettoyage de canapé à domicile.',
    "À partir de 80 € après crédit d'impôt. Injection-extraction professionnelle chez vous : les taches partent, les odeurs aussi, et le tissu retrouve sa teinte d'origine.",
    'canape-injection.jpg', '55% 40%',
    "J'identifie la fibre et je teste la tenue des couleurs sur une zone cachée avant d'appliquer quoi que ce soit. Puis détachage ciblé, brossage mécanisé et injection-extraction : de l'eau claire est injectée sous pression et réaspirée aussitôt avec la saleté. Bâche de protection au sol, rien à déplacer, séchage en quelques heures.",
    "Un canapé ne se salit pas qu'en surface.",
    [('drop', 'Taches alimentaires', "Café, vin, gras, chocolat, sauces : traitées une par une avec le détachant adapté."),
     ('leaf', "Traces d'animaux", "Poils incrustés, salive, petits accidents. Désinfection comprise à chaque passage."),
     ('sun', 'Transpiration et urine', "Les auréoles s'installent dans la mousse. L'extraction va les chercher en profondeur."),
     ('spark', 'Odeurs', "Tabac, humidité, renfermé. On ne masque pas avec un parfum : on retire ce qui sent.")],
    [('search', 'Diagnostic', "J'identifie la fibre et je teste la tenue des couleurs sur une zone cachée."),
     ('drop', 'Détachage', "Détachants ciblés selon chaque tache, puis brossage mécanisé sur toute l'assise."),
     ('clock', "Temps d'action", "Cinq minutes pour que le produit décolle la saleté incrustée dans la fibre."),
     ('vac', 'Injection-extraction', "Eau claire injectée sous pression puis réaspirée aussitôt, avec la saleté dissoute.")],
    ("Un prix ferme, annoncé avant de commencer.", "Tarif de départ pour un canapé deux places. Le prix définitif dépend du nombre de places, du tissu et de l'état : il vous est confirmé sur devis, avant toute intervention.",
     "Canapé deux places · à partir de", "160 €", "80 €", "Après crédit d'impôt de 50 %. Déplacement compris dans le prix annoncé."),
    ("Ce que je ne peux pas promettre.", "Un nettoyage professionnel retire la saleté. Il ne refait pas un canapé neuf, et certains dégâts sont définitifs. Je préfère le dire avant le devis.",
     ["Une décoloration causée par le soleil ou un produit ménager ne revient pas : la couleur est partie, il n'y a plus rien à retirer.",
      "Une tache d'encre, de teinture ou de javel modifie la fibre. Elle s'atténue parfois, elle ne disparaît pas.",
      "Un tissu usé jusqu'à la trame ressortira propre, mais toujours usé. Le nettoyage ne reconstitue pas une fibre.",
      "Une odeur qui revient signale presque toujours une mousse imprégnée. Un second passage est parfois nécessaire."],
     "Je vous dis sur place ce qui partira et ce qui ne partira pas, avant de commencer. Vous décidez ensuite."),
    canape_extra,
    [("Combien de temps le canapé met-il à sécher ?", "Entre 4 et 8 heures selon l'épaisseur de la mousse et l'aération de la pièce. Vous pouvez vous rasseoir dessus le soir même."),
     ("Faut-il déplacer le canapé ?", "Non. Je travaille sur place, avec une bâche de protection au sol. Vous n'avez rien à préparer."),
     ("Et si les taches ne partent pas ?", "Je vous le dis avant de commencer. Certaines taches anciennes ou décolorantes ne partent jamais totalement : je préfère vous prévenir plutôt que de vous vendre un miracle."),
     ("Traitez-vous les canapés en cuir ?", "Non. Le cuir et le simili ne se nettoient pas par injection-extraction. Je vous oriente plutôt vers un spécialiste du cuir."),
     credit_q],
    canape_gallery,
    "Nettoyage de canapé", "Nettoyage de canapé à domicile par injection-extraction dès 80 € après crédit d'impôt.",
    "Nettoyage de canapé à domicile dès 80 € — Val-d'Oise (95) | Divine Nettoyage",
    "Nettoyage de canapé à domicile par injection-extraction dès 80 € après crédit d'impôt. Val-d'Oise et Île-de-France. Devis gratuit sous 24 h.",
    "Votre canapé mérite <span class=\"gold\">mieux</span> qu'un remplacement.")

# --- matelas
matelas_gallery = f'''
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Avant / après</span><h2>La différence se voit.</h2></div>
    <div class="ba">
      <figure class="reveal"><img src="images/avant-apres-matelas.jpg" alt="Matelas d'enfant taché avant et après nettoyage" loading="lazy"><figcaption>Matelas enfant<span class="mono">Avant / Après</span></figcaption></figure>
      <div class="reveal" style="display:grid;gap:14px;align-content:center;padding:clamp(8px,3vw,32px)">
        <h3 style="font-size:1.6rem">Quand faire nettoyer son matelas&nbsp;?</h3>
        {checks(["<b>Une fois par an</b>, pour que la transpiration ne s'installe pas en profondeur", "<b>Après un accident</b> : plus on intervient tôt, plus le résultat est complet", "<b>En cas d'allergies</b> : un passage par an change le quotidien", "<b>Avant d'emménager</b> ou avant la première nuit dans un meublé", "<b>Après une maladie</b>, avant de reprendre son lit"], 'one')}
      </div>
    </div>
  </div>
</section>'''
textile_page('nettoyage-matelas.html', 'Nettoyage de matelas', 'Matelas', 'Nettoyage de matelas à domicile.',
    "À partir de 70 € après crédit d'impôt. Transpiration, acariens, auréoles : l'injection-extraction retire ce qu'un aspirateur ne peut pas atteindre, sans détremper la mousse.",
    'canape-angle-injection.jpg', '50% 55%',
    "On passe un tiers de sa vie sur son matelas. Aspiration profonde, traitement de chaque auréole selon son origine, désinfection sur toute la surface puis rinçage par injection-extraction. La mousse reste humide, jamais détrempée : vous dormez dessus le soir même si j'interviens le matin.",
    "Ce qu'un matelas accumule.",
    [('drop', 'Transpiration', "Près d'un demi-litre par nuit. Tout finit dans la mousse, et les auréoles jaunes suivent."),
     ('search', 'Acariens et allergènes', "Ils se logent dans les fibres profondes. L'extraction en élimine une grande partie."),
     ('bed', "Accidents d'enfants", "Pipi au lit, régurgitations, biberons renversés. Traités et désinfectés, odeur comprise."),
     ('spark', 'Odeurs de renfermé', "Matelas stocké, chambre peu aérée, humidité. On retire la cause, on ne la parfume pas.")],
    [('vac', 'Aspiration profonde', "Première passe pour retirer poussières, peaux mortes et poils avant toute humidification."),
     ('drop', 'Traitement des taches', "Chaque auréole est traitée avec le produit adapté à son origine, puis brossée."),
     ('shield', 'Désinfection', "Produit professionnel sur toute la surface, efficace sur les acariens et les bactéries."),
     ('spark', 'Injection-extraction', "Rinçage à l'eau claire et réaspiration immédiate. Humide, jamais détrempé.")],
    ("Un prix ferme, annoncé avant de commencer.", "Tarif de départ pour un matelas une place. Comptez un supplément pour un deux places ou un matelas à traiter sur les deux faces. Prix confirmé sur devis avant l'intervention.",
     "Matelas une place · à partir de", "140 €", "70 €", "Après crédit d'impôt de 50 %. Désinfection comprise."),
    ("Ce que je ne peux pas promettre.", "L'extraction retire beaucoup, mais pas tout. Autant être clair avant l'intervention.",
     ["Une auréole ancienne et jaunie s'éclaircit sans toujours disparaître : l'urine ou la transpiration ont modifié la fibre.",
      "Les acariens sont fortement réduits, jamais éliminés définitivement. Ils reviennent avec le temps.",
      "Un matelas à ressorts très ancien peut garder une odeur venant de sa structure interne, hors d'atteinte.",
      "Je ne traite ni les matelas déchirés ni ceux dont le coutil est perforé : l'eau entrerait sans ressortir."],
     "Comme toujours, je vous donne mon avis honnête avant de commencer, pas après."),
    '',
    [("Je peux dormir dessus le soir même ?", "Oui, si j'interviens le matin. Comptez 4 à 6 heures de séchage dans une pièce aérée."),
     ("Vous traitez les deux faces ?", "Sur demande. Le plus souvent, seule la face du dessus a besoin d'être traitée."),
     ("Est-ce que ça élimine vraiment les acariens ?", "L'extraction et la désinfection en retirent une grande partie, mais aucun professionnel honnête ne vous promettra une élimination totale et définitive : ils reviennent avec le temps. Un passage par an fait une vraie différence."),
     credit_q],
    matelas_gallery,
    "Nettoyage de matelas", "Nettoyage de matelas à domicile par injection-extraction dès 70 € après crédit d'impôt.",
    "Nettoyage de matelas à domicile dès 70 € — Val-d'Oise (95) | Divine Nettoyage",
    "Nettoyage de matelas à domicile par injection-extraction dès 70 € après crédit d'impôt. Acariens, auréoles, odeurs. Val-d'Oise et Île-de-France.",
    "Retrouvez un matelas <span class=\"gold\">sain</span>.")

# --- tapis
tapis_extra = f'''
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Les fibres</span><h2>Les fibres et ce qu'elles supportent.</h2><p>Un tapis n'est pas l'autre. Le test de la fibre décide de tout le reste.</p></div>
    <div class="tiles">
      <div class="tile reveal"><h3>Laine</h3><p>La plus noble et la plus fréquente. Supporte très bien l'extraction, à pression et température limitées. Séchage long, jusqu'à 8 heures.</p></div>
      <div class="tile reveal"><h3>Viscose et soie artificielle</h3><p>La matière la plus délicate. Elle jaunit et se raidit au contact de l'eau. Je teste systématiquement, et je renonce si le risque est réel.</p></div>
      <div class="tile reveal"><h3>Synthétique</h3><p>Polypropylène, polyamide, polyester : très tolérants. Les couleurs ressortent fort et le séchage est rapide.</p></div>
      <div class="tile reveal"><h3>Jute, sisal, fibres végétales</h3><p>Ces matières n'aiment pas l'eau : elles se tachent et se déforment. Je les traite à sec quand c'est possible, ou je refuse.</p></div>
      <div class="tile reveal"><h3>Moquettes</h3><p>Traitées au mètre carré, chez les particuliers comme dans les locaux professionnels. Même méthode, matériel adapté aux grandes surfaces.</p></div>
      <div class="tile reveal"><h3>Séchage</h3><p>De 2 à 8 heures selon l'épaisseur. Un tapis épais en laine met plus longtemps qu'un tapis fin en synthétique.</p></div>
    </div>
  </div>
</section>'''
textile_page('nettoyage-tapis.html', 'Nettoyage de tapis', 'Tapis', 'Nettoyage de tapis à domicile.',
    "À partir de 50 € après crédit d'impôt. L'injection-extraction ravive les couleurs sans agresser les fibres, à condition de tester la tenue des teintes avant de commencer.",
    'canape-modulable.jpg', '50% 70%',
    "Un tapis encaisse tout : le passage, la poussière, les taches. Je teste la fibre sur un coin, j'aspire énergiquement la saleté sèche, je détache et brosse, puis j'injecte de l'eau claire que je réaspire aussitôt. Les couleurs ressortent, le tapis n'est pas gorgé d'eau.",
    "Ce qu'un tapis retient.",
    [('home', 'Saleté de passage', "La poussière s'accumule à la base de la fibre et ternit la couleur bien avant qu'on voie une tache."),
     ('drop', 'Taches du quotidien', "Vin, café, encre, gras. Traitées une par une, selon la nature de la fibre."),
     ('leaf', 'Animaux', "Poils, salive, accidents. Désinfection et traitement des odeurs compris."),
     ('sun', 'Couleurs ternies', "Une fois la saleté retirée, les teintes d'origine ressortent. L'effet est souvent spectaculaire.")],
    [('search', 'Test de la fibre', "Laine, viscose, synthétique : je teste la tenue des couleurs sur un coin avant toute chose."),
     ('vac', 'Dépoussiérage', "Aspiration énergique pour retirer la saleté sèche, l'essentiel du volume."),
     ('brush', 'Détachage et brossage', "Détachants ciblés sur les taches, produit professionnel et brossage mécanisé."),
     ('spark', 'Injection-extraction', "Eau claire injectée puis réaspirée. Les couleurs ressortent, le tapis n'est pas détrempé.")],
    ("Un prix ferme, annoncé avant de commencer.", "Tarif de départ pour un petit tapis. Le prix suit les dimensions et la fibre : un tapis en laine ou en viscose demande plus de précautions qu'un synthétique. Envoyez une photo et les mesures, le prix est confirmé sous 24 h.",
     "Petit tapis · à partir de", "100 €", "50 €", "Après crédit d'impôt de 50 %. Moquettes au mètre carré, sur devis."),
    ("Ce que je ne peux pas promettre.", "Certains tapis ne se rattrapent pas, et certains ne doivent pas être mouillés du tout.",
     ["Un tapis en viscose déjà mouillé garde souvent des zones raides et jaunies. C'est irréversible.",
      "Une frange abîmée ou jaunie s'améliore, rarement complètement : la fibre y est la plus fine et la plus exposée.",
      "Un tapis qui dégorge au test de couleur ne sera pas traité à l'eau. Je refuse plutôt que de vous le rendre taché.",
      "Les brûlures et les trous relèvent de la restauration, un autre métier."],
     "Envoyez-moi une photo et les dimensions : je vous dis avant de me déplacer si le jeu en vaut la chandelle."),
    tapis_extra,
    [("Mon tapis est en laine, c'est possible ?", "Oui, avec un dosage et une pression adaptés. C'est exactement pour cela que je teste la fibre avant de commencer."),
     ("Combien de temps pour sécher ?", "De 2 à 8 heures selon l'épaisseur. Un tapis épais en laine met plus longtemps qu'un tapis fin."),
     ("Vous traitez aussi les moquettes ?", "Oui, au mètre carré, chez les particuliers comme dans les locaux professionnels. Demandez un devis."),
     credit_q],
    '',
    "Nettoyage de tapis et moquettes", "Nettoyage de tapis et moquettes à domicile dès 50 € après crédit d'impôt.",
    "Nettoyage de tapis à domicile dès 50 € — Val-d'Oise (95) | Divine Nettoyage",
    "Nettoyage de tapis et moquettes à domicile dès 50 € après crédit d'impôt. Laine, viscose, synthétique. Val-d'Oise et Île-de-France.",
    "Des couleurs qui <span class=\"gold\">ressortent</span>.")

# ================================================================= PROFESSIONNELS
pro_faq = [
    ("Pouvez-vous intervenir en dehors de nos horaires ?", "Oui. Nous intervenons avant l'ouverture ou après la fermeture pour ne jamais gêner votre activité."),
    ("Proposez-vous des contrats d'entretien ?", "Oui : passages mensuels, bimestriels ou trimestriels, créneau réservé à l'avance, tarif dégressif et facturation mensuelle."),
    ("Le crédit d'impôt s'applique-t-il aux entreprises ?", "Non. Le crédit d'impôt services à la personne concerne uniquement les particuliers, pour des prestations réalisées à leur domicile."),
    ("Êtes-vous assurés ?", f"Oui. Divine Nettoyage est une entreprise déclarée (SIRET {SIRET}) et assurée en responsabilité civile professionnelle auprès d'ORUS."),
]
pros = hero_page('vitrine.jpg', 'Professionnels', 'Professionnels', 'Dans vos locaux.',
    "Vitrines, bureaux, restaurants, hôtels et locations meublées. Un intervenant unique et identifié, des créneaux hors horaires d'ouverture et un devis ferme sous 24 h.", pos='50% 25%') + f'''
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Pour qui</span><h2>Commerces, bureaux<br>et locaux d'accueil.</h2></div>
    {tiles([('store', 'Commerces et vitrines', "Boutiques, agences, restaurants, salons. Passage avant l'ouverture ou après la fermeture."),
            ('build', 'Bureaux et tertiaire', "Cloisons vitrées, portes intérieures, garde-corps, halls d'immeuble."),
            ('brush', 'Fin de chantier', "Ciment, plâtre, silicone, éclats de peinture et adhésifs retirés à la lame."),
            ('pole', 'Locaux industriels', "Grandes surfaces vitrées, verrières et vitrages en hauteur, à la perche."),
            ('bed', 'Locations meublées', "Canapés, literie et moquettes entre deux locataires."),
            ('sofa', "Salles d'attente et accueils", "Chaises, banquettes et canapés d'accueil en tissu.")])}
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Trois types d'intervention</span><h2>Régulier, ponctuel<br>ou fin de chantier.</h2></div>
    <div class="tiles">
      <div class="tile reveal"><span class="ic">{ic('cal')}</span><h3>Entretien régulier</h3><p>Passage planifié à fréquence fixe pour des vitrages toujours nets. La formule des commerces dont la vitrine est la première impression.</p><ul><li>Mensuel, bimestriel ou trimestriel</li><li>Créneau réservé à l'avance</li><li>Tarif dégressif à l'abonnement</li></ul></div>
      <div class="tile reveal"><span class="ic">{ic('spark')}</span><h3>Nettoyage ponctuel</h3><p>Un grand nettoyage complet en une intervention : avant une réception, une mise en vente, une visite ou au changement de saison.</p><ul><li>Sans engagement</li><li>Intérieur et extérieur</li><li>Encadrements inclus</li></ul></div>
      <div class="tile reveal"><span class="ic">{ic('build')}</span><h3>Fin de chantier</h3><p>La prestation la plus technique : ciment, plâtre, silicone, peinture, adhésifs et étiquettes incrustés dans le verre.</p><ul><li>Grattage à la lame</li><li>Retrait des films et adhésifs</li><li>Décapage des dépôts calcaires</li></ul></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Comment ça se passe</span><h2>De la visite à la facture.</h2><p>Un interlocuteur unique, un devis ferme, et des passages qui ne gênent jamais votre activité.</p></div>
    {steps([('pin', 'Visite', "Je passe voir les surfaces, je relève les accès, les hauteurs et vos contraintes d'horaires."),
            ('doc', 'Devis sous 24 h', "Prix ferme, détaillé par poste, sans engagement. Vous savez exactement ce que vous payez."),
            ('cal', 'Intervention', "Créneau convenu à l'avance, avant l'ouverture ou après la fermeture si besoin."),
            ('shield', 'Contrôle', "Vérification ensemble avant mon départ, puis facture. Facturation mensuelle sur contrat.")])}
  </div>
</section>
<section class="section tight band">
  <div class="wrap split">
    <div class="reveal"><span class="eyebrow">Ce qui est compris</span><h2 style="margin-top:14px">Toujours inclus, jamais en supplément.</h2>
      <p>Le devis couvre l'intervention complète. Pas de ligne qui apparaît après coup. Une vitrine propre se remarque ; une vitrine sale aussi, et c'est la première chose que voit votre client.</p></div>
    <div class="reveal">{checks(["Lavage des deux faces lorsqu'elles sont accessibles", "Encadrements, rails et appuis nettoyés", "Protection du sol et du mobilier", "Travail en hauteur à la perche, sans échafaudage", "Évacuation de nos déchets", "Contrôle en contre-jour avant départ"], 'one')}</div>
  </div>
</section>
{faq_section(pro_faq, "Questions des professionnels")}
{cta(title_html="Un devis ferme <span class=\"gold\">sous 24 heures</span>.", text="Envoyez l'adresse du local et deux ou trois photos des surfaces à traiter : nous vous répondons avec un prix, sans engagement.", img='vitrine.jpg')}
'''
page('professionnels.html', "Nettoyage de vitrines, bureaux et fin de chantier — Val-d'Oise | Divine Nettoyage",
     "Nettoyage de vitrines, bureaux, locaux et fin de chantier pour les professionnels du Val-d'Oise et d'Île-de-France. Contrats d'entretien, devis ferme sous 24 h.",
     pros, jsonld=[BUSINESS, faq_ld(pro_faq)])

# ================================================================= CRÉDIT D'IMPÔT
credit = hero_page('jensen-veranda.jpg', "Crédit d'impôt", 'Services à la personne', "Vous ne réglez que la moitié.",
    "Nos prestations à domicile ouvrent droit au crédit d'impôt « services à la personne » : 50 % de la facture vous est rendu par l'État. Avec l'avance immédiate de l'Urssaf, vous n'avancez même pas cette moitié.",
    pos='50% 35%', cta_label='Vérifier mon éligibilité') + f'''
<section class="section">
  <div class="wrap split" style="align-items:center">
    <div class="reveal"><span class="eyebrow">Le principe</span><h2 style="margin-top:14px">Sur une facture de 100 €, vous en réglez 50.</h2>
      <p>L'autre moitié est prélevée par l'Urssaf, qui nous la verse directement. Vous ne faites aucune avance et vous n'avez rien à déclarer l'année suivante.</p>
      <p>Dispositif officiel d'avance immédiate du crédit d'impôt, mis en place par l'Urssaf et la Direction générale des Finances publiques. Nous passons par la coopérative <b>Unipros</b>, qui garantit un cadre administratif conforme et sécurisé. L'inscription est gratuite et sans engagement.</p></div>
    <div class="split-amount reveal">
      <div class="amount you"><b>50 €</b><h3>Votre part</h3><p>Réglée au moment de la prestation, comme n'importe quelle facture.</p></div>
      <div class="amount state"><b>50 €</b><h3>Pris en charge</h3><p>Prélevés par l'Urssaf et versés directement à l'entreprise.</p></div>
    </div>
  </div>
</section>
<section class="section band">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">En pratique</span><h2>Quatre étapes,<br>une seule de votre côté.</h2></div>
    {steps([('user', 'Inscription', "Nous vous inscrivons au dispositif. Vous validez votre compte Urssaf, gratuitement et sans engagement."),
            ('home', 'Intervention', "Nous réalisons la prestation à votre domicile et émettons la facture."),
            ('euro', 'Prélèvement', "L'Urssaf vous prélève la moitié du montant, directement et en toute sécurité."),
            ('check', 'Terminé', "Rien à avancer, rien à déclarer : l'autre moitié est réglée par l'État.")])}
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Les plafonds</span><h2>Jusqu'à quel montant&nbsp;?</h2><p>Le plafond est annuel et vaut pour l'ensemble de vos dépenses de services à la personne, tous prestataires confondus.</p></div>
    <div class="caps">
      <div class="cap reveal"><span class="mono">Cas général</span><b>6 000 €</b><p>de crédit d'impôt par an, pour 12 000 € de dépenses annuelles.</p></div>
      <div class="cap reveal"><span class="mono">Avec enfant ou personne de +65 ans</span><b>7 500 €</b><p>Majoration de 1 500 € par personne au foyer, pour 15 000 € de dépenses.</p></div>
      <div class="cap reveal"><span class="mono">Situation d'invalidité</span><b>10 000 €</b><p>de crédit d'impôt par an, pour 20 000 € de dépenses annuelles.</p></div>
    </div>
  </div>
</section>
<section class="section tight band">
  <div class="wrap compare">
    <div class="reveal"><h3><span class="eyebrow">Concerné</span></h3>{checks(["Lavage de vitres à votre domicile", "Nettoyage de canapés, matelas et tapis chez vous", "Toute prestation réalisée chez un particulier"])}</div>
    <div class="reveal"><h3><span class="mono" style="color:var(--ink-3)">Non concerné</span></h3>{checks(["Locaux professionnels et commerces", "Prestations réalisées ailleurs qu'à votre domicile"], 'x')}
      <p class="fine-note">Informations vérifiées en octobre 2026. Le crédit d'impôt services à la personne est maintenu intégralement pour 2026.</p></div>
  </div>
</section>
{cta(title_html="Profitez-en dès <span class=\"gold\">votre première intervention</span>.", text="Nous nous occupons de l'inscription, vous n'avez qu'à la valider.", img='jensen-portrait.jpg')}
'''
page('credit-impot.html', "Crédit d'impôt 50 % et avance immédiate Urssaf | Divine Nettoyage",
     "Nettoyage de vitres et de textiles à domicile : 50 % de crédit d'impôt avec l'avance immédiate de l'Urssaf via Unipros. Vous ne réglez que la moitié.",
     credit, jsonld=[BUSINESS])

# ================================================================= ZONES
dept_html = ''
order = ["Val-d'Oise (95)", "Paris (75)", "Hauts-de-Seine (92)", "Seine-Saint-Denis (93)", "Val-de-Marne (94)", "Yvelines (78)", "Essonne (91)", "Seine-et-Marne (77)"]
for d in order:
    cs = ZONES[d]
    if d.startswith('Paris'):
        cs = ['Paris 1er au 20e arrondissement']
    lis = ''.join(f'<li>{c}</li>' for c in cs)
    n = '20 arrondissements' if d.startswith('Paris') else f'{len(cs)} communes'
    dept_html += f'<div class="dept reveal" id="d{d[-3:-1]}"><h3>{d.split(" (")[0]}<small>{d[-4:]} · {n}</small></h3><ul>{lis}</ul></div>'
zones = hero_page('vitres-exterieur.jpg', "Zones d'intervention", 'Zones', "Le Val-d'Oise et toute l'Île-de-France.",
    "Nettoyage de canapés, de matelas, de tapis et de vitres dans les huit départements franciliens et le sud de l'Oise. Le déplacement est compris dans le prix annoncé.", pos='50% 30%') + f'''
<section class="section">
  <div class="wrap">
    <div class="shead"><span class="eyebrow">Commune par commune</span><h2>Nos deux métiers,<br>partout en Île-de-France.</h2>
      <p>Votre commune n'est pas citée ? Elle est très probablement desservie. Nous intervenons aussi en limite de l'Oise (60), à Chambly, Chantilly et dans les communes voisines.</p></div>
    {dept_html}
  </div>
</section>
{cta()}
'''
page('zones.html', "Zones d'intervention — Val-d'Oise et Île-de-France | Divine Nettoyage",
     "Nettoyage de canapé, matelas, tapis et vitres à domicile dans le Val-d'Oise (95), à Paris et dans toute l'Île-de-France. Liste des communes desservies.",
     zones, jsonld=[BUSINESS])
print('ok')

# ================================================================= DEVIS (assistant en 4 étapes)
CATALOG = [
    ('canape', 'sofa', 'Canapé ou fauteuil', 'Tissu, velours, microfibre, alcantara', [
        ('canape2', 'Canapé 2 places', 'dès 160 € · 80 € après crédit d\'impôt', 160),
        ('canape3', 'Canapé 3 places', 'Prix selon le tissu et l\'état', None),
        ('canapeAngle', 'Canapé d\'angle ou modulable', 'Prix selon la taille', None),
        ('fauteuil', 'Fauteuil', 'Sur devis', None),
        ('chaise', 'Chaise ou banquette', 'Sur devis, à l\'unité', None)]),
    ('matelas', 'bed', 'Matelas', 'Auréoles, acariens, accidents, odeurs', [
        ('matelas1', 'Matelas une place', 'dès 140 € · 70 € après crédit d\'impôt', 140),
        ('matelas2', 'Matelas deux places', 'Supplément, sur devis', None)]),
    ('tapis', 'rug', 'Tapis ou moquette', 'Laine, synthétique, viscose', [
        ('tapisPetit', 'Petit tapis', 'dès 100 € · 50 € après crédit d\'impôt', 100),
        ('tapisGrand', 'Grand tapis', 'Prix selon les dimensions', None),
        ('moquette', 'Moquette (par pièce)', 'Au mètre carré, sur devis', None)]),
    ('auto', 'car', 'Sièges de voiture', 'Banquette, sièges avant, coffre', [
        ('voiture', 'Véhicule', 'Sur devis', None)]),
    ('vitres', 'win', 'Fenêtres et baies vitrées', 'Intérieur et extérieur, encadrements compris', [
        ('fenetre', 'Fenêtre battante', 'S\'ouvre vers l\'intérieur', None),
        ('coulissant', 'Fenêtre coulissante', 'Les vitres glissent l\'une derrière l\'autre', None),
        ('baie', 'Baie vitrée ou porte-fenêtre', 'Descend jusqu\'au sol', None),
        ('velux', 'Fenêtre de toit', 'Posée dans la pente du toit', None),
        ('miroir', 'Miroir ou paroi de douche', 'Détartrage et polissage', None)]),
    ('veranda', 'veranda', 'Véranda, verrière, abri de piscine', 'Toitures et parois vitrées', [
        ('verandaU', 'Véranda ou verrière', 'Sur devis', None),
        ('abri', 'Abri de piscine', 'Sur devis', None),
        ('gardecorps', 'Garde-corps vitré', 'Balcon, terrasse, escalier', None)]),
    ('commerce', 'store', 'Vitrine ou local professionnel', 'Vitrines, bureaux, fin de chantier', [
        ('vitrine', 'Vitrine de commerce', 'Façade, porte vitrée, sas', None),
        ('bureaux', 'Bureaux ou cloisons vitrées', 'Sur devis', None),
        ('chantier', 'Fin de chantier', 'Plâtre, peinture, adhésifs', None)]),
    ('autre', 'cam', 'Autre chose', 'Une photo suffit pour vous répondre', [
        ('autreU', 'Autre surface ou objet', 'Décrivez-le à l\'étape 3', None)]),
]

def stepper(iid, name, sub, price):
    p = '' if price is None else f' data-price="{price}"'
    return (f'<div class="it" data-id="{iid}" data-name="{html.escape(name)}"{p}>'
            f'<div class="it-tx"><b>{name}</b><span>{sub}</span></div>'
            f'<div class="qty"><button type="button" class="q-minus" aria-label="Retirer : {html.escape(name)}">−</button>'
            f'<output aria-live="polite">0</output>'
            f'<button type="button" class="q-plus" aria-label="Ajouter : {html.escape(name)}">+</button></div></div>')

cats = ''
for cid, icon, title, sub, items in CATALOG:
    rows = ''.join(stepper(*i) for i in items)
    cats += (f'<div class="cat" id="c-{cid}" data-cat="{cid}">'
             f'<button type="button" class="cat-h" aria-expanded="false" aria-controls="p-{cid}">'
             f'<span class="cat-ic">{ic(icon)}</span><span class="cat-tx"><b>{title}</b><span>{sub}</span></span>'
             f'<span class="cat-n" hidden>0</span><span class="cat-chev">{ic("down")}</span></button>'
             f'<div class="cat-p" id="p-{cid}" hidden>{rows}</div></div>')

def seg(name, opts, checked=0):
    out = ''
    for i, o in enumerate(opts):
        oid = f'{name}-{i}'
        out += f'<input type="radio" id="{oid}" name="{name}" value="{o}"{" checked" if i == checked else ""}><label for="{oid}">{o}</label>'
    return f'<div class="seg">{out}</div>'

def photo_slot(i):
    n = '' if i == 1 else str(i)
    return (f'<label class="ph-slot" for="photo{i}"><input type="file" id="photo{i}" name="attachment{n}" accept="image/*">'
            f'<span class="ph-empty">{ic("cam")}<b>Photo {i}</b><small>Choisir une image</small></span>'
            f'<img alt="" hidden><button type="button" class="ph-del" aria-label="Retirer la photo {i}" hidden>{ic("close")}</button></label>')

devis_head = '<link rel="stylesheet" href="assets/devis.css">'
devis_body = f'''
<section class="wz-wrap">
  <div class="wz">
    <div class="wz-top">
      <p class="mono wz-count">Étape <b id="wz-n">1</b> sur 4 · <span id="wz-label">Vos besoins</span></p>
      <div class="wz-bar" aria-hidden="true"><i id="wz-fill"></i></div>
    </div>

    <form id="devis" action="https://formsubmit.co/{MAIL}" method="POST" enctype="multipart/form-data" novalidate>
      <input type="hidden" name="_subject" value="Nouvelle demande de devis — site Divine Nettoyage">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_captcha" value="false">
      <input type="hidden" name="_next" id="f-next" value="">
      <input type="text" name="_honey" class="sr-only" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="hidden" name="Prestation" id="f-presta">
      <input type="hidden" name="Estimation" id="f-estim">

      <fieldset class="wz-step" data-step="1" data-label="Vos besoins">
        <legend><h1>Que faut-il nettoyer&nbsp;?</h1></legend>
        <p class="wz-lede">Touchez ce qui correspond, puis comptez les éléments. Vous pouvez en combiner plusieurs : textiles et vitres le même jour.</p>
        <div class="cats">{cats}</div>
        <p class="wz-help">Un doute entre deux choix&nbsp;? Prenez le plus proche : Jensen ajuste avec vous avant de commencer. Les photos de l'étape 3 l'aident à chiffrer au plus juste.</p>
        <p class="wz-err" id="err-1" hidden>Ajoutez au moins un élément à nettoyer pour continuer.</p>
      </fieldset>

      <fieldset class="wz-step" data-step="2" data-label="Où et quand" hidden>
        <legend><h1>Où et quand&nbsp;?</h1></legend>
        <p class="wz-lede">Ces informations servent à préparer l'intervention et à vérifier votre éligibilité au crédit d'impôt.</p>
        <div class="fld"><span class="lbl">Vous êtes</span>
          <div class="cards2">
            <input type="radio" id="pr-0" name="Profil" value="Particulier" checked><label for="pr-0">{ic('home')}<b>Particulier</b><small>Crédit d'impôt de 50 %</small></label>
            <input type="radio" id="pr-1" name="Profil" value="Professionnel"><label for="pr-1">{ic('store')}<b>Professionnel</b><small>Commerce, bureau, location</small></label>
          </div></div>
        <div class="fld"><label class="lbl" for="f-cp">Code postal et ville</label><input id="f-cp" name="Code postal et ville" type="text" autocomplete="postal-code" placeholder="95000 Cergy" required></div>
        <div class="fld"><span class="lbl">Fréquence</span>{seg('Frequence', ['Ponctuel', 'Mensuel', 'Trimestriel', '2 fois par an'])}</div>
        <div class="row2">
          <div class="fld"><label class="lbl" for="f-date">Date souhaitée <small>facultatif</small></label><input id="f-date" name="Date souhaitee" type="date"></div>
          <div class="fld"><span class="lbl">Créneau préféré</span>{seg('Creneau', ['Matin', 'Après-midi', 'Soirée', 'Peu importe'], 3)}</div>
        </div>
        <p class="wz-err" id="err-2" hidden>Indiquez votre code postal et votre ville.</p>
      </fieldset>

      <fieldset class="wz-step" data-step="3" data-label="Photos" hidden>
        <legend><h1>Des photos&nbsp;?</h1></legend>
        <p class="wz-lede">Facultatif, mais ça change tout : une photo du canapé, du matelas ou des vitres permet de vous donner un prix précis sans se déplacer. Les images sont réduites automatiquement avant l'envoi.</p>
        <div class="ph-grid">{photo_slot(1)}{photo_slot(2)}{photo_slot(3)}</div>
        <div class="fld"><label class="lbl" for="f-msg">Précisions <small>facultatif</small></label><textarea id="f-msg" name="Message" rows="4" placeholder="Taches, dimensions, matière, étage, accès, animaux…"></textarea></div>
      </fieldset>

      <fieldset class="wz-step" data-step="4" data-label="Coordonnées" hidden>
        <legend><h1>Vos coordonnées</h1></legend>
        <p class="wz-lede">Jensen vous rappelle personnellement sous 24 heures pour confirmer le prix et le créneau.</p>
        <div class="fld"><label class="lbl" for="f-nom">Nom ou entreprise</label><input id="f-nom" name="Nom" type="text" autocomplete="name" required></div>
        <div class="row2">
          <div class="fld"><label class="lbl" for="f-tel">Téléphone</label><input id="f-tel" name="Telephone" type="tel" autocomplete="tel" inputmode="tel" placeholder="06 00 00 00 00" required></div>
          <div class="fld"><label class="lbl" for="f-mail">E-mail <small>facultatif</small></label><input id="f-mail" name="email" type="email" autocomplete="email" placeholder="vous@exemple.fr"></div>
        </div>
        <div class="recap" id="recap"></div>
        <p class="wz-fine">Demande sans engagement : ce n'est pas une réservation ferme. Vos coordonnées et vos photos servent uniquement à traiter votre demande. Elles ne sont ni revendues ni utilisées à d'autres fins.</p>
        <p class="wz-err" id="err-4" hidden>Indiquez votre nom et un numéro de téléphone valide.</p>
        <p class="wz-err" id="err-send" hidden></p>
      </fieldset>
    </form>

    <div class="wz-done" id="wz-done" hidden>
      <span class="done-ic">{ic('check')}</span>
      <h1>Merci, votre demande est bien arrivée.</h1>
      <p>Jensen vous rappelle sous 24 heures pour confirmer le prix et convenir d'un créneau. Pressé&nbsp;? Appelez directement le <a href="{TEL_HREF}">{TEL}</a>.</p>
      <a class="btn btn-dark" href="index.html">Retour à l'accueil</a>
    </div>
  </div>
</section>

<div class="wz-foot" id="wz-foot">
  <div class="wz-foot-in">
    <div class="wz-sum"><b id="sum-t">Aucun élément</b><span id="sum-s">Ajoutez ce qu'il faut nettoyer</span></div>
    <div class="wz-btns">
      <button type="button" class="btn btn-line" id="wz-prev" hidden>Retour</button>
      <button type="button" class="btn btn-dark" id="wz-next">Continuer</button>
    </div>
  </div>
</div>
'''
page('devis.html', "Devis gratuit en ligne | Divine Nettoyage",
     "Demandez votre devis gratuit de nettoyage de vitres, canapé, matelas ou tapis en 2 minutes. Réponse sous 24 h, crédit d'impôt de 50 % pour les particuliers.",
     devis_body, light=True, extra_head=devis_head, scripts='<script src="assets/devis.js"></script>')
# le pied de page n'a pas sa place sous l'assistant : il reste, mais on garde une marge pour la barre fixe
print('devis ok')
