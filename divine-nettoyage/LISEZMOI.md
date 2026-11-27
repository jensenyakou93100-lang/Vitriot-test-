# Site Divine Nettoyage

Site statique (HTML, CSS, JS, sans outil à installer) : 9 pages, prêtes à remplacer celles de divinenettoyage.fr.
Les adresses des anciennes pages sont conservées (`nettoyage-vitres.html`, `nettoyage-canape.html`…), donc le référencement Google n'est pas perdu.

## Mettre en ligne (Hostinger)

1. Ouvrir le gestionnaire de fichiers du site, dossier `public_html`.
2. Garder une copie de l'ancien site (télécharger le dossier), au cas où.
3. Envoyer **tout le contenu de ce dossier, sauf `_outils/` et ce fichier**.
4. Ouvrir divinenettoyage.fr et envoyer une demande de test depuis la page Devis.

Les demandes de devis partent par FormSubmit vers Divinetextile.pro@gmail.com, comme sur l'ancien site.

## Modifier le site

Les pages sont générées par `_outils/build.py` (textes, prix, avis, communes). Après une modification :

```
python3 _outils/build.py .
```

Le style est dans `assets/style.css`, le devis en 4 étapes dans `assets/devis.js` et `assets/devis.css`.
