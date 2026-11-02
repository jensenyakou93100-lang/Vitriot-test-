"""Sous-titres karaoké au format ASS (libass) : 2 à 4 mots, le mot prononcé en or."""
import re
import subprocess
from pathlib import Path

from PIL import ImageFont

from .config import Config
from .transcription import Mot
from .zones_sures import Boite

FIN_DE_PHRASE = re.compile(r"[.!?…:;]$")
VIRGULE = re.compile(r",$")
PHRASE_ETALON = "canapé propre"  # courte : doit tenir largement dans l’écran
COLLE_AU_PRECEDENT = ("'", "’", "-")


def recoller(mots: list[Mot]) -> list[Mot]:
    """Whisper coupe les élisions et les traits d'union (« n » + « 'avait », « injecteur » + « -extracteur ») :
    on les recolle en un seul mot."""
    resultat = []
    for m in mots:
        if resultat and m.texte.startswith(COLLE_AU_PRECEDENT):
            p = resultat[-1]
            colle = m.texte.replace("'", "’") if m.texte[0] in "'’" else m.texte
            resultat[-1] = Mot(p.debut, m.fin, p.texte + colle, min(p.confiance, m.confiance))
        else:
            resultat.append(m)
    return resultat


def _couleur_ass(hexa: str) -> str:
    """#RRGGBB → &H00BBGGRR (ordre inversé propre au format ASS)."""
    h = hexa.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def _temps(t: float) -> str:
    t = max(0.0, t)
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def _echapper(texte: str) -> str:
    return texte.replace("\\", "").replace("{", "(").replace("}", ")")


def grouper(mots: list[Mot], cfg: Config) -> list[list[Mot]]:
    """Découpe en petits groupes lisibles : coupure aux fins de phrase, aux pauses,
    à 4 mots, ou dès que la ligne deviendrait trop large."""
    st = cfg.rendu["sous_titres"]
    police = ImageFont.truetype(str(cfg.police(st["police"])), 100)
    facteur = _etalonner(cfg)
    largeur_max = cfg.largeur - 2 * cfg.rendu["zones_sures"]["marge_cotes"] - 2 * (st["contour"] + st["ombre"]) - 10

    def largeur(groupe):
        return police.getlength(_texte(groupe, st)) * facteur

    groupes, courant = [], []
    for mot in mots:
        if courant:
            precedent = courant[-1]
            couper = (
                len(courant) >= st["mots_max"]
                or FIN_DE_PHRASE.search(precedent.texte)
                or (VIRGULE.search(precedent.texte) and len(courant) >= st["mots_min"])
                or mot.debut - precedent.fin > st["pause_coupure"]
                or largeur(courant + [mot]) > largeur_max
            )
            if couper:
                groupes.append(courant)
                courant = []
        courant.append(mot)
    if courant:
        groupes.append(courant)

    groupes = _equilibrer(groupes, st, largeur, largeur_max)

    # Un mot isolé en début de phrase est rattaché au groupe suivant s'il y a la place
    fusion = []
    i = 0
    while i < len(groupes):
        g = groupes[i]
        if (len(g) == 1 and i + 1 < len(groupes) and not FIN_DE_PHRASE.search(g[0].texte)
                and len(groupes[i + 1]) < st["mots_max"]
                and groupes[i + 1][0].debut - g[0].fin <= st["pause_coupure"]
                and largeur(g + groupes[i + 1]) <= largeur_max):
            fusion.append(g + groupes[i + 1])
            i += 2
        else:
            fusion.append(g)
            i += 1
    return fusion


MOTS_OUTILS = {"le", "la", "les", "l’", "un", "une", "des", "du", "de", "d’", "au", "aux", "à", "et", "ou",
               "pour", "par", "avec", "sans", "sur", "dans", "en", "que", "qui", "ce", "cette", "ces",
               "mon", "ma", "mes", "son", "sa", "ses", "votre", "vos", "notre", "nos", "je", "tu", "il",
               "elle", "on", "nous", "vous", "ils", "elles", "ne", "n’", "très", "plus"}


def _equilibrer(groupes, st, largeur, largeur_max):
    """Évite les coupures maladroites quand un groupe a été coupé parce qu'il était plein :
    – ne jamais finir un groupe sur un petit mot (« depuis des | années. ») ;
    – ne pas laisser un mot seul en fin de phrase."""
    for i in range(len(groupes) - 1):
        a, b = groupes[i], groupes[i + 1]
        if FIN_DE_PHRASE.search(a[-1].texte) or VIRGULE.search(a[-1].texte):
            continue
        if b[0].debut - a[-1].fin > st["pause_coupure"]:
            continue
        a_bouger = 0
        if a[-1].texte.lower() in MOTS_OUTILS:
            a_bouger = 1
            if len(a) >= 3 and a[-2].texte.lower() in MOTS_OUTILS:
                a_bouger = 2
        elif len(b) == 1 and len(a) >= 3:
            a_bouger = 1
        if a_bouger and len(a) - a_bouger >= 1 and len(b) + a_bouger <= st["mots_max"] \
                and largeur(a[-a_bouger:] + b) <= largeur_max:
            groupes[i], groupes[i + 1] = a[:-a_bouger], a[-a_bouger:] + b
    return groupes


def _texte(groupe, st, actif=None, couleur_active=None):
    morceaux = []
    for i, m in enumerate(groupe):
        t = _echapper(m.texte.upper() if st.get("majuscules") else m.texte)
        morceaux.append(f"{{\\c{couleur_active}}}{t}{{\\c&H00FFFFFF&}}" if i == actif else t)
    return " ".join(morceaux)


def _entete(cfg: Config, contour=None, ombre=None) -> list[str]:
    st = cfg.rendu["sous_titres"]
    contour = st["contour"] if contour is None else contour
    ombre = st["ombre"] if ombre is None else ombre
    nom_police = ImageFont.truetype(str(cfg.police(st["police"]))).getname()[0]
    marge_v = cfg.hauteur - st["bas_du_texte"]
    marge_c = cfg.rendu["zones_sures"]["marge_cotes"]
    return [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {cfg.largeur}", f"PlayResY: {cfg.hauteur}",
        "WrapStyle: 2", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
        "MarginL, MarginR, MarginV, Encoding",
        f"Style: Karaoke,{nom_police},{st['taille']},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,"
        f"100,100,0,0,1,{contour},{ombre},2,{marge_c},{marge_c},{marge_v},1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]


_etalons = {}


def _etalonner(cfg: Config) -> float:
    """Combien de pixels libass dessine pour 1 pixel calculé par Pillow (taille 100).
    Mesuré une fois en faisant dessiner une phrase étalon par libass."""
    st = cfg.rendu["sous_titres"]
    cle = (st["police"], st["taille"])
    if cle not in _etalons:
        fichier = cfg.dossier_cache / f"etalon_{st['taille']}.ass"
        fichier.write_text("\n".join(_entete(cfg, contour=0, ombre=0)
                                     + [f"Dialogue: 0,0:00:00.00,0:00:05.00,Karaoke,,0,0,0,,{PHRASE_ETALON}"]) + "\n",
                           encoding="utf-8")
        boite = mesurer(fichier, cfg, 0.3)
        reel = (boite.x1 - boite.x0) if boite else st["taille"] * 6
        pillow = ImageFont.truetype(str(cfg.police(st["police"])), 100).getlength(PHRASE_ETALON)
        _etalons[cle] = reel / pillow
    return _etalons[cle]


def ecrire_ass(mots: list[Mot], cfg: Config, sortie: Path, fin_max: float):
    """Écrit le fichier .ass. Un événement par mot : le groupe reste affiché,
    seul le mot en cours de prononciation passe en or."""
    st = cfg.rendu["sous_titres"]
    or_ass = _couleur_ass(cfg.couleur("or")) + "&"
    lignes = _entete(cfg)
    groupes = grouper(recoller([m for m in mots if m.debut < fin_max]), cfg)
    for n, g in enumerate(groupes):
        debut = g[0].debut
        suivant = groupes[n + 1][0].debut if n + 1 < len(groupes) else fin_max
        fin = min(g[-1].fin + st["tenue_apres"], suivant, fin_max)
        for i, m in enumerate(g):
            t0 = debut if i == 0 else m.debut
            t1 = fin if i == len(g) - 1 else g[i + 1].debut
            if t1 - t0 < 0.01:
                continue
            lignes.append(f"Dialogue: 0,{_temps(t0)},{_temps(t1)},Karaoke,,0,0,0,,{_texte(g, st, i, or_ass)}")
    Path(sortie).write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return groupes


def chemin_filtre(p: Path) -> str:
    """Chemin utilisable à l'intérieur d'un filtre ffmpeg (Windows compris)."""
    return str(Path(p).resolve()).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def mesurer(fichier_ass: Path, cfg: Config, duree: float) -> Boite | None:
    """Mesure les pixels RÉELLEMENT dessinés par libass (contour compris) sur toute la durée.
    C'est cette mesure qui sert au contrôle des zones sûres, pas un calcul théorique."""
    polices = chemin_filtre(cfg.racine / "polices")
    filtre = (f"ass='{chemin_filtre(fichier_ass)}':fontsdir='{polices}',"
              f"lutyuv=y='if(between(val,118,134),0,255)',bbox=min_val=200")
    res = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-f", "lavfi", "-i",
         f"color=c=0x808080:s={cfg.largeur}x{cfg.hauteur}:r=10:d={duree:.2f}",
         "-vf", filtre, "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    x0 = y0 = 10 ** 6
    x1 = y1 = -1
    for m in re.finditer(r"x1:(\d+) x2:(\d+) y1:(\d+) y2:(\d+)", res.stderr):
        a, b, c, d = map(int, m.groups())
        x0, x1, y0, y1 = min(x0, a), max(x1, b), min(y0, c), max(y1, d)
    if x1 < 0:
        return None
    return Boite("sous-titres", x0, y0, x1 + 1, y1 + 1)
