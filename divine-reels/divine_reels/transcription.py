"""Étape 2 : transcription locale avec faster-whisper, horodatage AU MOT, mise en cache."""
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from .cache import empreinte, empreinte_fichier
from .config import Config
from .erreurs import ErreurDivine

VERSION = 1
FREQUENCE = 16000
_modele_charge = {}


@dataclass
class Mot:
    debut: float
    fin: float
    texte: str
    confiance: float = 1.0

    def decale(self, delta: float) -> "Mot":
        return Mot(round(self.debut + delta, 3), round(self.fin + delta, 3), self.texte, self.confiance)


def _audio_brut(fichier: Path):
    """Son du fichier en mono 16 kHz, extrait par ffmpeg (plus robuste que la lecture interne de Whisper)."""
    import numpy as np
    res = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i", str(fichier), "-vn", "-ac", "1", "-ar", str(FREQUENCE),
         "-f", "s16le", "-"], capture_output=True)
    if res.returncode != 0:
        raise ErreurDivine(f"Impossible d'extraire le son de {Path(fichier).name}.")
    return np.frombuffer(res.stdout, np.int16).astype(np.float32) / 32768.0


def _modele(cfg: Config):
    nom = cfg.rendu["transcription"]["modele"]
    if nom not in _modele_charge:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            raise ErreurDivine("faster-whisper n'est pas installé. Relancez le script d'installation.")
        print(f"   🧠 Chargement du modèle de transcription « {nom} »…")
        try:
            _modele_charge[nom] = WhisperModel(nom, device="cpu", compute_type="int8")
        except Exception:
            raise ErreurDivine(f"Modèle de transcription « {nom} » introuvable sur cet ordinateur. "
                               "Relancez le script d'installation (il le télécharge une seule fois).")
    return _modele_charge[nom]


def transcrire(fichier: Path, cfg: Config) -> list[Mot]:
    """Liste des mots prononcés avec leur début et leur fin (en secondes).
    Un fichier déjà transcrit n'est jamais retranscrit."""
    reglages = cfg.rendu["transcription"]
    dossier = cfg.dossier_cache / "transcriptions"
    dossier.mkdir(exist_ok=True)
    cle = empreinte(empreinte_fichier(fichier), reglages, VERSION)
    cache = dossier / f"{cle}.json"
    if cache.exists():
        return [Mot(**m) for m in json.loads(cache.read_text(encoding="utf-8"))]

    print(f"   🎙️  Transcription de {Path(fichier).name}…")
    segments, _ = _modele(cfg).transcribe(
        _audio_brut(fichier), language="fr", word_timestamps=True, vad_filter=True,
        initial_prompt=reglages.get("vocabulaire") or None,
    )
    mots = []
    for seg in segments:
        for w in seg.words or []:
            texte = w.word.strip()
            if texte:
                mots.append(Mot(round(w.start, 3), round(w.end, 3), texte, round(w.probability, 2)))
    cache.write_text(json.dumps([asdict(m) for m in mots], ensure_ascii=False, indent=1), encoding="utf-8")
    return mots
