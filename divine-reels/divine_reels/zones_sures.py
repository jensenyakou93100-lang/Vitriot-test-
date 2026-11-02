"""Règle absolue : aucun texte dans les zones mortes d'Instagram."""
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import Config


@dataclass
class Boite:
    """Rectangle occupé par un texte, en pixels sur l'image finale 1080×1920."""
    nom: str
    x0: int
    y0: int
    x1: int
    y1: int


def zone_permise(cfg: Config) -> tuple:
    z = cfg.rendu["zones_sures"]
    return z["marge_cotes"], z["haut"], cfg.largeur - z["marge_cotes"], cfg.hauteur - z["bas"]


def controler(boites: list[Boite], cfg: Config) -> list[str]:
    """Renvoie la liste des textes qui débordent, expliqués en français."""
    gauche, haut, droite, bas = zone_permise(cfg)
    problemes = []
    for b in boites:
        if b.y0 < haut:
            problemes.append(f"« {b.nom} » entre dans la zone morte du HAUT ({haut - b.y0} px de trop)")
        if b.y1 > bas:
            problemes.append(f"« {b.nom} » entre dans la zone morte du BAS ({b.y1 - bas} px de trop)")
        if b.x0 < gauche or b.x1 > droite:
            problemes.append(f"« {b.nom} » déborde sur les CÔTÉS")
    return problemes


def enregistrer(boites: list[Boite], chemin: Path):
    Path(chemin).write_text(json.dumps([asdict(b) for b in boites], ensure_ascii=False, indent=1), encoding="utf-8")


def lire(chemin: Path) -> list[Boite]:
    return [Boite(**d) for d in json.loads(Path(chemin).read_text(encoding="utf-8"))]
