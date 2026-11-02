"""Appels à ffmpeg / ffprobe, avec des erreurs lisibles."""
import json
import shutil
import subprocess
from pathlib import Path

from .erreurs import ErreurDivine


def verifier_installation():
    for outil in ("ffmpeg", "ffprobe"):
        if shutil.which(outil) is None:
            raise ErreurDivine(f"{outil} n'est pas installé. Relancez le script d'installation.")


def lancer(args: list, quoi: str) -> str:
    """Lance ffmpeg. En cas d'échec, montre seulement les dernières lignes utiles."""
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-y", "-loglevel", "error", *map(str, args)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        detail = "\n".join(res.stderr.strip().splitlines()[-4:])
        raise ErreurDivine(f"Échec pendant : {quoi}.\n   Détail ffmpeg : {detail}")
    return res.stderr


def analyser(args: list) -> str:
    """Lance ffmpeg pour une analyse (sortie dans stderr, niveau info)."""
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", *map(str, args)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return res.stderr


def sonder(fichier: Path) -> dict:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(fichier)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if res.returncode != 0:
        raise ErreurDivine(f"Impossible de lire {Path(fichier).name} : fichier abîmé ou format inconnu.")
    return json.loads(res.stdout)


def flux(info: dict, type_: str):
    return next((s for s in info.get("streams", []) if s.get("codec_type") == type_), None)


def rotation(flux_video: dict) -> int:
    """Rotation enregistrée par le téléphone (0, 90, 180, 270)."""
    rot = 0
    for sd in flux_video.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    rot = int(flux_video.get("tags", {}).get("rotate", rot))
    return abs(rot) % 360


def dimensions_affichees(flux_video: dict) -> tuple:
    """Largeur × hauteur telles qu'on les voit à l'écran (rotation du téléphone comprise)."""
    l, h = int(flux_video["width"]), int(flux_video["height"])
    if rotation(flux_video) in (90, 270):
        l, h = h, l
    return l, h


def duree(info: dict) -> float:
    return float(info.get("format", {}).get("duration", 0) or 0)
