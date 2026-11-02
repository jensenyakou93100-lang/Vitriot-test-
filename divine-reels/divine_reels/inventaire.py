"""Étape 1 : inventaire des rushes (durée, format, orientation, son, netteté)."""
import json
import re
import subprocess
from dataclasses import asdict, dataclass, field
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat

from . import ffmpeg
from .cache import empreinte_fichier
from .config import Config
from .erreurs import ErreurDivine

EXTENSIONS = {".mp4", ".mov", ".m4v"}


@dataclass
class Rush:
    chemin: str
    nom: str
    empreinte: str
    duree: float
    largeur: int
    hauteur: int
    fps: float
    a_du_son: bool
    volume_moyen: float | None   # en dB, None si pas de piste son
    nettete: float
    alertes: list = field(default_factory=list)

    @property
    def vertical(self) -> bool:
        return self.hauteur > self.largeur

    @property
    def role(self) -> str:
        """Préfixe du nom de fichier : avant_, geste_, apres_, face_, accroche_."""
        prefixe = self.nom.split("_", 1)[0].lower()
        return prefixe if prefixe in {"avant", "geste", "apres", "face", "accroche"} else "autre"


def _nettete(chemin: Path, instant: float) -> float:
    """Netteté d'une image du milieu du rush (variance du contour : bas = flou)."""
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-ss", f"{instant:.2f}", "-i", str(chemin),
           "-frames:v", "1", "-vf", "scale=540:-2", "-f", "image2pipe", "-vcodec", "png", "-"]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0 or not res.stdout:
        return 0.0
    img = Image.open(BytesIO(res.stdout)).convert("L")
    laplacien = img.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128))
    return round(ImageStat.Stat(laplacien).var[0], 1)


def _volume_moyen(chemin: Path) -> float | None:
    sortie = ffmpeg.analyser(["-i", str(chemin), "-vn", "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume:\s*(-?[\d.]+|-inf) dB", sortie)
    if not m:
        return None
    return -91.0 if m.group(1) == "-inf" else float(m.group(1))


def analyser_rush(chemin: Path, cfg: Config) -> Rush:
    cache = cfg.dossier_cache / "inventaire"
    cache.mkdir(exist_ok=True)
    emp = empreinte_fichier(chemin)
    fichier_cache = cache / f"{emp}.json"
    if fichier_cache.exists():
        donnees = json.loads(fichier_cache.read_text(encoding="utf-8"))
        donnees.update(chemin=str(chemin), nom=chemin.stem)
        return Rush(**donnees)

    info = ffmpeg.sonder(chemin)
    video = ffmpeg.flux(info, "video")
    if video is None:
        raise ErreurDivine(f"{chemin.name} ne contient pas d'image.")
    largeur, hauteur = ffmpeg.dimensions_affichees(video)
    num, _, den = video.get("avg_frame_rate", "30/1").partition("/")
    fps = round(float(num) / float(den or 1), 2) if float(den or 1) else 30.0
    duree = ffmpeg.duree(info)
    a_du_son = ffmpeg.flux(info, "audio") is not None

    rush = Rush(
        chemin=str(chemin), nom=chemin.stem, empreinte=emp, duree=round(duree, 2),
        largeur=largeur, hauteur=hauteur, fps=fps, a_du_son=a_du_son,
        volume_moyen=_volume_moyen(chemin) if a_du_son else None,
        nettete=_nettete(chemin, duree / 2),
    )
    reglages = cfg.rendu["inventaire"]
    if not rush.vertical:
        rush.alertes.append("vidéo HORIZONTALE : elle sera fortement recadrée (on perd les côtés)")
    if rush.nettete < reglages["seuil_flou"]:
        rush.alertes.append(f"image qui semble FLOUE (netteté {rush.nettete:.0f}, minimum conseillé {reglages['seuil_flou']})")
    if not a_du_son:
        rush.alertes.append("aucune piste son")
    elif rush.volume_moyen is not None and rush.volume_moyen < reglages["seuil_silence"]:
        rush.alertes.append(f"rush quasi SILENCIEUX (volume moyen {rush.volume_moyen:.0f} dB)")
    if hauteur < 1280:
        rush.alertes.append(f"petite résolution ({largeur}×{hauteur}) : l'image sera un peu molle")

    donnees = asdict(rush)
    fichier_cache.write_text(json.dumps(donnees, ensure_ascii=False, indent=1), encoding="utf-8")
    return rush


def inventorier(dossier: Path, cfg: Config) -> list[Rush]:
    dossier = Path(dossier)
    if not dossier.is_dir():
        raise ErreurDivine(f"Dossier de rushes introuvable : {dossier}")
    fichiers = sorted(p for p in dossier.iterdir() if p.suffix.lower() in EXTENSIONS and not p.name.startswith("."))
    if not fichiers:
        raise ErreurDivine(f"Aucune vidéo (.mp4, .mov) dans {dossier}")
    return [analyser_rush(p, cfg) for p in fichiers]


def afficher(rushes: list[Rush]):
    print(f"\n📋 Inventaire : {len(rushes)} rush(es)\n")
    for r in rushes:
        son = "muet" if r.volume_moyen is None else f"{r.volume_moyen:.0f} dB"
        sens = "vertical" if r.vertical else "HORIZONTAL"
        print(f"  • {r.nom:<28} {r.duree:5.1f} s  {r.largeur}×{r.hauteur} {sens:<10} son {son:<7} [{r.role}]")
        for a in r.alertes:
            print(f"      ⚠️  {a}")
    total = sum(r.duree for r in rushes)
    print(f"\n  Durée totale des rushes : {total:.1f} s\n")
