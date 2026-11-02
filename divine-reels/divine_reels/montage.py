"""Assemblage : rushes mis au format 1080×1920 + carte de fin."""
from pathlib import Path

from . import cartons, ffmpeg, zones_sures
from .cache import empreinte
from .config import Config
from .erreurs import ErreurDivine
from .inventaire import Rush

VERSION = 1  # à augmenter quand la façon de normaliser change (invalide le cache)


def _parametres_video(cfg: Config) -> dict:
    return {"l": cfg.largeur, "h": cfg.hauteur, "fps": cfg.fps, "v": VERSION}


def normaliser(rush: Rush, cfg: Config) -> Path:
    """Met un rush au format exact : 1080×1920, 30 i/s, son stéréo 48 kHz.
    Résultat mis en cache : un rush n'est normalisé qu'une seule fois."""
    dossier = cfg.dossier_cache / "normalises"
    dossier.mkdir(exist_ok=True)
    sortie = dossier / f"{rush.empreinte}_{empreinte(_parametres_video(cfg))}.mp4"
    if sortie.exists():
        return sortie

    L, H, fps = cfg.largeur, cfg.hauteur, cfg.fps
    freq = cfg.rendu["encodage"]["audio_frequence"]
    # « cover » : on remplit tout l'écran, quitte à rogner les bords (jamais de bandes noires)
    filtre_video = (f"scale={L}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
                    f"crop={L}:{H},setsar=1,fps={fps},format=yuv420p")
    args = ["-i", rush.chemin]
    if rush.a_du_son:
        carte_audio = ["-map", "0:a:0", "-af", f"aresample={freq},aformat=channel_layouts=stereo"]
    else:
        args += ["-f", "lavfi", "-i", f"anullsrc=r={freq}:cl=stereo"]
        carte_audio = ["-map", "1:a", "-shortest"]
    temporaire = sortie.with_suffix(".tmp.mp4")
    ffmpeg.lancer([
        *args, "-map", "0:v:0", *carte_audio, "-vf", filtre_video,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
        "-c:a", "aac", "-b:a", "256k", "-ar", freq, "-ac", 2,
        temporaire,
    ], f"mise au format de {rush.nom}")
    temporaire.rename(sortie)
    return sortie


def carte_de_fin(cfg: Config) -> tuple[Path, list]:
    """Vidéo de la carte de fin (2 s, son coupé net). En cache tant que la marque ne change pas."""
    dossier = cfg.dossier_cache / "cartes"
    dossier.mkdir(exist_ok=True)
    cle = empreinte(cfg.marque["carte_fin"], cfg.marque["couleurs"], cfg.marque["polices"],
                    cfg.rendu["zones_sures"], _parametres_video(cfg))
    image, video, boites_json = dossier / f"fin_{cle}.png", dossier / f"fin_{cle}.mp4", dossier / f"fin_{cle}.json"
    if not (video.exists() and boites_json.exists()):
        boites = cartons.carte_de_fin(cfg, image)
        problemes = zones_sures.controler(boites, cfg)
        if problemes:
            raise ErreurDivine("La carte de fin ne respecte pas les zones sûres :\n   " + "\n   ".join(problemes))
        freq = cfg.rendu["encodage"]["audio_frequence"]
        temporaire = video.with_suffix(".tmp.mp4")
        ffmpeg.lancer([
            "-loop", 1, "-framerate", cfg.fps, "-i", image,
            "-f", "lavfi", "-i", f"anullsrc=r={freq}:cl=stereo",
            "-t", cfg.marque["carte_fin"]["duree"],
            "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "256k", temporaire,
        ], "fabrication de la carte de fin")
        temporaire.rename(video)
        zones_sures.enregistrer(boites, boites_json)
    return video, zones_sures.lire(boites_json)


def assembler(rushes: list[Rush], cfg: Config, sortie: Path) -> dict:
    """Colle les rushes (dans l'ordre) puis la carte de fin, et encode le fichier final.
    Renvoie ce qu'il faut savoir pour la vérification."""
    duree_fin = cfg.marque["carte_fin"]["duree"]
    budget = cfg.rendu["duree"]["maximum"] - duree_fin - 0.5   # place disponible pour les images
    morceaux, total, coupes = [], 0.0, []
    for rush in rushes:
        if total >= budget:
            coupes.append(rush.nom)
            continue
        garde = min(rush.duree, budget - total)
        morceaux.append((normaliser(rush, cfg), garde))
        if garde < rush.duree - 0.05:
            coupes.append(f"{rush.nom} (raccourci à {garde:.1f} s)")
        total += garde

    video_fin, boites = carte_de_fin(cfg)
    morceaux.append((video_fin, duree_fin))

    entrees, filtres, etiquettes = [], [], []
    for i, (fichier, duree) in enumerate(morceaux):
        entrees += ["-i", fichier]
        filtres.append(f"[{i}:v]trim=0:{duree:.3f},setpts=PTS-STARTPTS[v{i}];"
                       f"[{i}:a]atrim=0:{duree:.3f},asetpts=PTS-STARTPTS[a{i}]")
        etiquettes.append(f"[v{i}][a{i}]")
    a = cfg.rendu["audio"]
    freq = cfg.rendu["encodage"]["audio_frequence"]
    graphe = ";".join(filtres) + ";" + "".join(etiquettes) + f"concat=n={len(morceaux)}:v=1:a=1[v][a0];" \
        f"[a0]loudnorm=I={a['loudness_cible']}:TP={a['crete_max'] - 0.5}:LRA=11,aresample={freq}[a]"

    enc = cfg.rendu["encodage"]
    temporaire = sortie.with_name(sortie.stem + ".en-cours.mp4")
    ffmpeg.lancer([
        *entrees, "-filter_complex", graphe, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", enc["preset"], "-crf", enc["crf"], "-profile:v", "high",
        "-maxrate", enc["debit_max"], "-bufsize", "24M", "-pix_fmt", "yuv420p", "-r", cfg.fps,
        "-c:a", "aac", "-b:a", enc["audio_debit"], "-ar", freq, "-ac", 2,
        "-movflags", "+faststart", temporaire,
    ], "encodage de la vidéo finale")
    return {"temporaire": temporaire, "boites": boites, "coupes": coupes,
            "duree_images": round(total, 2)}
