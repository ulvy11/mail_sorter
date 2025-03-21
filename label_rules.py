LABELS_WITH_RULES = {
    "astek": "si il fait référence à natixis, ou astek",
    "mutuelle": "si il fait référence à MMA ou mercer",
    "banque": "si il provient du Crédit Agricole",
    "animestore": "si l'expéditeur est anime store",
    "famille": "si dans les expéditeurs il y a donat doan-van ou muriel doan-van ou balthazar garcia",
    "emilie": "si l'expéditeur est emilie berthe (emilie.erthe@gmail.com)",
    "sncf": "si il provient de la sncf",
    "cogito": "si il vient de kisskissbankbank et fait référence à Cogito ou esprit critique",
    "entretiens": "si il fait référence à un entretien professionnel à venir ou passé",
    "factures": "si le mail fait référence à un achat effectué sur internet (facture, confirmation de commande, livraison, souscription etc.); ou si c'est une souscription à Allianz",
    "poubelle": "si le mail est une publicité ou provient de linkedin ou de Qwertee ou d'Uber eats",
    "newsletter": "si le mail est une newsletter",
}


def prompt_rules() -> str:
    res = ""
    for label, rule in LABELS_WITH_RULES.items():
        res += f'- "{label}" : {rule}\n'
    # removing final EOL
    return res[:-1]


TO_CLASSIFY = "to_classify"
EXPECTED_LABELS = [label for label in LABELS_WITH_RULES.keys()] + [TO_CLASSIFY]

TRANSFORMATION_RULES = {
    "banque": "banques/crédit agricole",
    "astek": "travail/Astek",
    "anime\\_store": "anime store",
    "animestore": "anime store",
    "cogito": "esprit critique",
}
