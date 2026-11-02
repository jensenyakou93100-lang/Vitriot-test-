"""Images fixes générées avec Pillow : carte de fin (et plus tard accroche, carte prix)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import Config
from .zones_sures import Boite, zone_permise

SUR = 2  # on dessine en double taille puis on réduit : bords bien lisses


def _rgb(hexa: str) -> tuple:
    hexa = hexa.lstrip("#")
    return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))


def police_ajustee(chemin: Path, taille: int, texte: str, largeur_max: int) -> ImageFont.FreeTypeFont:
    """Réduit la taille de police jusqu'à ce que le texte tienne en largeur."""
    while taille > 10:
        police = ImageFont.truetype(str(chemin), taille)
        if police.getlength(texte) <= largeur_max:
            return police
        taille = int(taille * 0.94)
    return ImageFont.truetype(str(chemin), taille)


def dessiner_etoile(draw: ImageDraw.ImageDraw, cx: float, cy: float, rayon: float, couleur):
    """Étoile à quatre branches ✦ (signature de la marque)."""
    r_int = rayon * 0.26
    d = r_int * 0.7071
    points = [
        (cx, cy - rayon), (cx + d, cy - d), (cx + rayon, cy), (cx + d, cy + d),
        (cx, cy + rayon), (cx - d, cy + d), (cx - rayon, cy), (cx - d, cy - d),
    ]
    draw.polygon(points, fill=couleur)


STYLES_FIN = {
    # style : (rôle de police, taille, couleur, espace avant)
    "titre":     ("titre",      116, "creme", 46),
    "info":      ("texte",       58, "creme", 34),
    "telephone": ("texte_gras", 104, "or",    92),
    "site":      ("texte",       56, "creme", 40),
}


def carte_de_fin(cfg: Config, sortie: Path) -> list[Boite]:
    """Dessine la carte de fin et renvoie la position de chaque texte (pour le contrôle des zones sûres)."""
    L, H = cfg.largeur * SUR, cfg.hauteur * SUR
    img = Image.new("RGB", (L, H), _rgb(cfg.couleur("brun")))
    draw = ImageDraw.Draw(img)
    gauche, haut, droite, bas = (v * SUR for v in zone_permise(cfg))
    largeur_max = (droite - gauche) - 40 * SUR

    # 1. Préparer chaque élément et mesurer la hauteur totale
    rayon = 70 * SUR
    elements = []
    hauteur_totale = 2 * rayon
    for ligne in cfg.marque["carte_fin"]["lignes"]:
        role, taille, couleur, espace = STYLES_FIN[ligne["style"]]
        police = police_ajustee(cfg.police(role), taille * SUR, ligne["texte"], largeur_max)
        x0, y0, x1, y1 = draw.textbbox((0, 0), ligne["texte"], font=police, anchor="ls")
        elements.append((ligne["texte"], police, _rgb(cfg.couleur(couleur)), espace * SUR, -y0, y1))
        hauteur_totale += espace * SUR + (y1 - y0)

    # 2. Centrer le bloc dans la zone sûre
    y = haut + ((bas - haut) - hauteur_totale) / 2
    dessiner_etoile(draw, L / 2, y + rayon, rayon, _rgb(cfg.couleur("or")))
    boites = [Boite("étoile ✦", int((L / 2 - rayon) / SUR), int(y / SUR), int((L / 2 + rayon) / SUR), int((y + 2 * rayon) / SUR))]
    y += 2 * rayon

    for texte, police, couleur, espace, montee, descente in elements:
        y += espace
        ligne_base = y + montee
        draw.text((L / 2, ligne_base), texte, font=police, fill=couleur, anchor="ms")
        x0, y0, x1, y1 = draw.textbbox((L / 2, ligne_base), texte, font=police, anchor="ms")
        boites.append(Boite(texte, int(x0 / SUR), int(y0 / SUR), int(x1 / SUR + 0.99), int(y1 / SUR + 0.99)))
        y = ligne_base + descente

    img = img.resize((cfg.largeur, cfg.hauteur), Image.LANCZOS)
    img.save(sortie)
    return boites

