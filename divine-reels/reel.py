#!/usr/bin/env python3
"""divine-reels — transforme des rushes de téléphone en vidéos verticales prêtes à publier.

Exemples :
    python reel.py --rushes ./chantier-taverny --modele transformation
    python reel.py --rushes ./chantier-taverny --inventaire
"""
import argparse
import sys
import time
import traceback
from pathlib import Path

RACINE = Path(__file__).resolve().parent
sys.path.insert(0, str(RACINE))

from divine_reels import config, ffmpeg, inventaire, montage, verification  # noqa: E402
from divine_reels.cache import empreinte  # noqa: E402
from divine_reels.erreurs import ErreurDivine, RenduRefuse  # noqa: E402


class Arguments(argparse.ArgumentParser):
    def error(self, message):
        if "--rushes" in message and "required" in message:
            message = "il manque --rushes suivi du dossier de vidéos"
        sys.exit(f"\n❌ Commande incomplète ou incorrecte : {message}.\n"
                 f"   Exemple : python reel.py --rushes ./chantier-taverny --modele transformation\n"
                 f"   Aide complète : python reel.py --aide")


def lire_arguments():
    p = Arguments(prog="reel.py", add_help=False,
                  description="Usine à variantes de vidéos verticales — Divine Nettoyage")
    p.add_argument("--rushes", required=True, type=Path, help="dossier contenant les vidéos filmées au téléphone")
    p.add_argument("--modele", default="transformation", help="nom du modèle (dossier modeles/)")
    p.add_argument("--inventaire", action="store_true", help="seulement analyser les rushes, sans rien produire")
    p.add_argument("--sortie", type=Path, help="dossier de sortie (par défaut : sorties/<nom du dossier de rushes>)")
    p.add_argument("--aide", "-h", action="help", help="afficher cette aide")
    return p.parse_args()


def trier(rushes, modele):
    ordre = modele.get("ordre_plans", [])
    rang = {role: i for i, role in enumerate(ordre)}
    return sorted(rushes, key=lambda r: (rang.get(r.role, len(ordre)), r.nom))


def principal():
    args = lire_arguments()
    ffmpeg.verifier_installation()
    cfg = config.charger()
    modele = config.charger_modele(args.modele)

    rushes = inventaire.inventorier(args.rushes, cfg)
    inventaire.afficher(rushes)
    if args.inventaire:
        return

    rushes = trier(rushes, modele)
    dossier_sortie = args.sortie or (RACINE / "sorties" / args.rushes.resolve().name)
    dossier_sortie.mkdir(parents=True, exist_ok=True)
    final = dossier_sortie / f"{modele['nom']}_base.mp4"

    # Idempotence : si rien n'a changé (rushes, modèle, réglages), on ne refait rien.
    cle = empreinte([r.empreinte for r in rushes], modele, cfg.marque, cfg.rendu, montage.VERSION)
    fichier_cle = final.with_name("." + final.name + ".cle")
    if final.exists() and fichier_cle.exists() and fichier_cle.read_text() == cle:
        print(f"✅ Déjà à jour, rien à refaire : {final}")
        return

    debut = time.time()
    print(f"🎬 Montage « {modele['nom']} » : {len(rushes)} rush(es) + carte de fin…")
    resultat = montage.assembler(rushes, cfg, final)
    for c in resultat["coupes"]:
        print(f"   ✂️  trop long pour tenir en {cfg.rendu['duree']['maximum']} s : {c}")

    print("🔎 Vérification du rendu…")
    problemes, mesures = verification.verifier(resultat["temporaire"], cfg, resultat["boites"])
    if problemes:
        rejet = dossier_sortie / "_refuses"
        rejet.mkdir(exist_ok=True)
        resultat["temporaire"].replace(rejet / final.name)
        raise RenduRefuse(final.name, problemes)
    resultat["temporaire"].replace(final)
    fichier_cle.write_text(cle)

    print(f"\n✅ Terminé en {time.time() - debut:.0f} s : {final}")
    print(f"   {mesures['resolution']} · {mesures['duree']} s · {mesures['taille_mo']} Mo · "
          f"crête son {mesures.get('crete_db', 0):.1f} dB · {mesures['textes_controles']} textes dans les zones sûres")


if __name__ == "__main__":
    try:
        principal()
    except RenduRefuse as e:
        sys.exit(f"\n❌ {e}\n   Le fichier n'a PAS été livré (copie mise de côté dans _refuses/).")
    except ErreurDivine as e:
        sys.exit(f"\n❌ {e}")
    except KeyboardInterrupt:
        sys.exit("\n⏹  Arrêté à votre demande. Relancez la même commande pour reprendre là où ça s'est arrêté.")
    except Exception:
        journal = RACINE / "erreur.log"
        journal.write_text(traceback.format_exc(), encoding="utf-8")
        sys.exit(f"\n❌ Erreur inattendue. Le détail technique est dans {journal.name} "
                 f"(à m'envoyer si le problème se répète).")
