"""Erreurs « propres » : elles portent un message en français destiné à l'utilisateur."""


class ErreurDivine(Exception):
    """Erreur attendue, expliquée en clair. Jamais de trace technique à l'écran."""


class RenduRefuse(ErreurDivine):
    """Un rendu a échoué à la vérification finale."""

    def __init__(self, fichier, problemes):
        self.fichier = fichier
        self.problemes = problemes
        lignes = "\n".join(f"   ✗ {p}" for p in problemes)
        super().__init__(f"Rendu refusé : {fichier}\n{lignes}")
