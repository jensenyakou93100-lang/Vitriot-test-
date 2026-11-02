"""Assemblage : rushes mis au format 1080×1920 + carte de fin."""
from pathlib import Path

from . import cartons, ffmpeg, sous_titres, transcription, zones_sures
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


def assembler(rushes: list[Rush], cfg: Config, sortie: Path, voix: Path | None = None) -> dict:
    """Colle les rushes (dans l'ordre), ajoute voix-off et sous-titres, puis la carte de fin.
    Renvoie ce qu'il faut savoir pour la vérification."""
    duree_fin = cfg.marque["carte_fin"]["duree"]
    budget = cfg.rendu["duree"]["maximum"] - duree_fin - 0.5   # place disponible pour les images
    duree_voix = 0.0
    if voix:
        duree_voix = ffmpeg.duree(ffmpeg.sonder(voix))
        if duree_voix > budget:
            raise ErreurDivine(f"La voix-off dure {duree_voix:.0f} s : c'est trop long. Maximum {budget:.0f} s "
                               f"(la vidéo fait {cfg.rendu['duree']['maximum']} s, carte de fin comprise).")
        budget = min(budget, duree_voix + 0.4)

    # 1. Placer les rushes sur la ligne de temps
    segments, total, coupes = [], 0.0, []
    for rush in rushes:
        if total >= budget - 0.05:
            coupes.append(rush.nom)
            continue
        garde = min(rush.duree, budget - total)
        segments.append((rush, normaliser(rush, cfg), total, garde))
        if garde < rush.duree - 0.05:
            coupes.append(f"{rush.nom} (raccourci à {garde:.1f} s)")
        total += garde
    alertes = []
    if voix and total < duree_voix:
        alertes.append(f"pas assez d'images ({total:.1f} s) pour couvrir la voix-off ({duree_voix:.1f} s)")

    # 2. Mots prononcés, recalés sur la ligne de temps
    if voix:
        mots = [m for m in transcription.transcrire(voix, cfg) if m.fin <= total]
    else:
        mots = []
        for rush, _, debut, garde in segments:
            if rush.a_du_son:
                mots += [m.decale(debut) for m in transcription.transcrire(Path(rush.chemin), cfg) if m.fin <= garde]

    # 3. Sous-titres karaoké
    boites_st, fichier_ass, groupes = [], None, []
    if mots:
        dossier = cfg.dossier_cache / "sous_titres"
        dossier.mkdir(exist_ok=True)
        fichier_ass = dossier / f"{empreinte([vars(m) for m in mots], cfg.rendu['sous_titres'], cfg.marque['couleurs'], total)}.ass"
        groupes = sous_titres.ecrire_ass(mots, cfg, fichier_ass, fin_max=total)
        boite = sous_titres.mesurer(fichier_ass, cfg, total)
        if boite:
            boites_st.append(boite)

    video_fin, boites = carte_de_fin(cfg)
    morceaux = [(f, g) for _, f, _, g in segments] + [(video_fin, duree_fin)]

    # 4. Graphe ffmpeg
    entrees, filtres, etiquettes = [], [], []
    for i, (fichier, duree) in enumerate(morceaux):
        entrees += ["-i", fichier]
        filtres.append(f"[{i}:v]trim=0:{duree:.3f},setpts=PTS-STARTPTS[v{i}];"
                       f"[{i}:a]atrim=0:{duree:.3f},asetpts=PTS-STARTPTS[a{i}]")
        etiquettes.append(f"[v{i}][a{i}]")
    a = cfg.rendu["audio"]
    freq = cfg.rendu["encodage"]["audio_frequence"]
    graphe = ";".join(filtres) + ";" + "".join(etiquettes) + f"concat=n={len(morceaux)}:v=1:a=1[vc][ac]"
    if fichier_ass:
        polices = sous_titres.chemin_filtre(cfg.racine / "polices")
        graphe += f";[vc]ass='{sous_titres.chemin_filtre(fichier_ass)}':fontsdir='{polices}'[v]"
    else:
        graphe += ";[vc]null[v]"
    if voix:
        k = len(morceaux)
        entrees += ["-i", voix]
        graphe += (f";[{k}:a:0]aresample={freq},aformat=channel_layouts=stereo,"
                   f"atrim=0:{total:.3f},apad=whole_dur={total + duree_fin:.3f}[vx]"
                   f";[ac]volume={cfg.rendu['voix_off']['ambiance_db']}dB[amb]"
                   f";[amb][vx]amix=inputs=2:duration=first:normalize=0[am]")
    else:
        graphe += ";[ac]anull[am]"
    graphe += f";[am]loudnorm=I={a['loudness_cible']}:TP={a['crete_max'] - 0.5}:LRA=11,aresample={freq}[a]"

    enc = cfg.rendu["encodage"]
    temporaire = sortie.with_name(sortie.stem + ".en-cours.mp4")
    ffmpeg.lancer([
        *entrees, "-filter_complex", graphe, "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", enc["preset"], "-crf", enc["crf"], "-profile:v", "high",
        "-maxrate", enc["debit_max"], "-bufsize", "24M", "-pix_fmt", "yuv420p", "-r", cfg.fps,
        "-c:a", "aac", "-b:a", enc["audio_debit"], "-ar", freq, "-ac", 2,
        "-movflags", "+faststart", temporaire,
    ], "encodage de la vidéo finale")
    return {"temporaire": temporaire, "boites": boites + boites_st, "coupes": coupes, "alertes": alertes,
            "duree_images": round(total, 2), "mots": len(mots), "groupes": len(groupes), "ass": fichier_ass}
