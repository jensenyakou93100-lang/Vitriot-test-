"""Chargement des fichiers YAML de configuration."""
from dataclasses import dataclass
from pathlib import Path

import yaml

from .erreurs import ErreurDivine

RACINE = Path(__file__).resolve().parent.parent


def _lire_yaml(chemin: Path) -> dict:
    if not chemin.exists():
        raise ErreurDivine(f"Fichier de configuration introuvable : {chemin}")
    try:
        with open(chemin, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        ligne = getattr(getattr(e, "problem_mark", None), "line", None)
        ou = f" (vers la ligne {ligne + 1})" if ligne is not None else ""
        raise ErreurDivine(f"Le fichier {chemin.name} est mal écrit{ou}. Vérifiez les guillemets et les décalages.")


@dataclass
class Config:
    marque: dict
    rendu: dict
    racine: Path = RACINE

    @property
    def largeur(self) -> int:
        return self.rendu["format"]["largeur"]

    @property
    def hauteur(self) -> int:
        return self.rendu["format"]["hauteur"]

    @property
    def fps(self) -> int:
        return self.rendu["format"]["images_par_seconde"]

    def couleur(self, nom: str) -> str:
        return self.marque["couleurs"][nom]

    def police(self, role: str) -> Path:
        chemin = self.racine / "polices" / self.marque["polices"][role]
        if not chemin.exists():
            raise ErreurDivine(f"Police manquante : {chemin.name} (dossier polices/). Relancez l'installation.")
        return chemin

    @property
    def dossier_cache(self) -> Path:
        d = self.racine / ".cache"
        d.mkdir(exist_ok=True)
        return d


def charger(racine: Path = RACINE) -> Config:
    return Config(
        marque=_lire_yaml(racine / "config" / "marque.yaml"),
        rendu=_lire_yaml(racine / "config" / "rendu.yaml"),
        racine=racine,
    )


def charger_modele(nom: str, racine: Path = RACINE) -> dict:
    chemin = racine / "modeles" / f"{nom}.yaml"
    if not chemin.exists():
        dispo = sorted(p.stem for p in (racine / "modeles").glob("*.yaml"))
        raise ErreurDivine(f"Modèle « {nom} » inconnu. Modèles disponibles : {', '.join(dispo)}")
    modele = _lire_yaml(chemin)
    modele.setdefault("nom", nom)
    return modele
