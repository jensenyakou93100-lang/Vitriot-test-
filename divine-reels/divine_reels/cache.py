"""Empreintes de fichiers : on ne refait jamais un travail déjà fait."""
import hashlib
import json
from pathlib import Path

_MO = 1024 * 1024


def empreinte_fichier(chemin: Path) -> str:
    """Empreinte rapide : taille + début + fin du fichier (pas besoin de lire 2 Go)."""
    chemin = Path(chemin)
    h = hashlib.sha1()
    taille = chemin.stat().st_size
    h.update(str(taille).encode())
    with open(chemin, "rb") as f:
        h.update(f.read(_MO))
        if taille > 2 * _MO:
            f.seek(-_MO, 2)
            h.update(f.read(_MO))
    return h.hexdigest()[:16]


def empreinte(*elements) -> str:
    """Empreinte d'un ensemble de réglages (dictionnaires, textes, empreintes de fichiers)."""
    brut = json.dumps(elements, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(brut.encode("utf-8")).hexdigest()[:16]


def empreinte_code() -> str:
    """Empreinte du code de l'outil : après une mise à jour, les rendus finaux sont refaits."""
    dossier = Path(__file__).resolve().parent
    h = hashlib.sha1()
    for f in sorted(dossier.glob("*.py")):
        h.update(f.read_bytes())
    return h.hexdigest()[:16]
