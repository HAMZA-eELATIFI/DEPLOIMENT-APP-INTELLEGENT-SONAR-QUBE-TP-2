HIGH_RISK_THRESHOLD = 0.6
MEDIUM_RISK_THRESHOLD = 0.3


def calculate_risk(income, debt):
    """Retourne le niveau de risque de crédit selon le ratio dette / revenu.

    Retourne -1 si le revenu est nul ou négatif (entrée invalide).
    """
    if income <= 0:
        return -1

    ratio = debt / income

    if ratio > HIGH_RISK_THRESHOLD:
        return "HIGH"
    if ratio > MEDIUM_RISK_THRESHOLD:
        return "MEDIUM"
    return "LOW"
