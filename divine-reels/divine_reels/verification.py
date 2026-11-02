"""Contrôle de chaque rendu AVANT de le déclarer terminé."""
import re
from pathlib import Path

from . import ffmpeg, zones_sures
from .config import Config


def crete_audio(fichier: Path) -> float | None:
    """Niveau le plus fort du son, en dBFS (0 = saturation)."""
    sortie = ffmpeg.analyser(["-i", str(fichier), "-vn", "-af", "astats=measure_perchannel=none", "-f", "null", "-"])
    valeurs = re.findall(r"Peak level dB:\s*(-?[\d.]+|-inf)", sortie)
    if not valeurs:
        return None
    return max(-120.0 if v == "-inf" else float(v) for v in valeurs)


def verifier(fichier: Path, cfg: Config, boites: list) -> tuple[list, dict]:
    """Renvoie (problèmes, mesures). Aucun problème = rendu accepté."""
    problemes, mesures = [], {}
    info = ffmpeg.sonder(fichier)
    video, audio = ffmpeg.flux(info, "video"), ffmpeg.flux(info, "audio")

    # 1. Format
    if video is None:
        return ["aucune image dans le fichier"], mesures
    l, h = ffmpeg.dimensions_affichees(video)
    mesures["resolution"] = f"{l}×{h}"
    if (l, h) != (cfg.largeur, cfg.hauteur):
        problemes.append(f"résolution {l}×{h} au lieu de {cfg.largeur}×{cfg.hauteur}")
    if video.get("codec_name") != "h264":
        problemes.append(f"codec vidéo {video.get('codec_name')} au lieu de H.264")
    if video.get("pix_fmt") != "yuv420p":
        problemes.append(f"format de couleur {video.get('pix_fmt')} (certains téléphones ne le liront pas)")

    # 2. Durée
    d = ffmpeg.duree(info)
    mesures["duree"] = round(d, 2)
    dmin, dmax = cfg.rendu["duree"]["minimum"], cfg.rendu["duree"]["maximum"]
    if not dmin <= d <= dmax + 0.05:
        problemes.append(f"durée {d:.1f} s hors de la plage autorisée ({dmin} à {dmax} s)")

    # 3. Taille
    mo = Path(fichier).stat().st_size / 1024 / 1024
    mesures["taille_mo"] = round(mo, 1)
    if mo >= cfg.rendu["verification"]["taille_max_mo"]:
        problemes.append(f"fichier trop lourd : {mo:.0f} Mo (maximum {cfg.rendu['verification']['taille_max_mo']} Mo)")

    # 4. Son
    if audio is None or audio.get("codec_name") != "aac":
        problemes.append("pas de piste son AAC")
    else:
        crete = crete_audio(fichier)
        mesures["crete_db"] = crete
        if crete is not None and crete > cfg.rendu["verification"]["crete_refus"]:
            problemes.append(f"son SATURÉ (crête à {crete:.1f} dB)")

    # 5. Zones sûres
    problemes += zones_sures.controler(boites, cfg)
    mesures["textes_controles"] = len(boites)
    return problemes, mesures
