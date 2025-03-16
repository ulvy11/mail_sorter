import ollama
from ollama import Message
from pprint import pprint

from label_rules import TO_CLASSIFY, prompt_rules

PROMPT_UNDERSTOOD = "Je suis prêt à renvoyer une catégorie pour chaque mail."

MISTRAL_MAIL_MANAGER_PROMPT_NEVER_BODY = f"""
    tu es un assitant de messagerie, ton rôle est de lire des emails reçus, de déterminer la catégorie correspondant parmi les règles suivantes dans l'ordre :
        {prompt_rules()}
    Si un mail ne fait référence à aucune de ces situations, détermine la catégorie toi-même EN UN SEUL MOT.

    Voici le format de réponse que tu dois me fournir : "<categorie>"
    Je ne veux pas de résumé
    Ne formule pas de phrase, ne me répond QUE la catégorie en UN SEUL MOT EN MINUSCULE SANS QUOTES AUTOUR DU MOT

    Ce que je vais t'envoyer aura cette forme:

        Voici l'expéditeur du mail à catégoriser : ""\"{{expediteur}}""\"
        Voici l'objet du mail à catégoriser :  ""\"{{objet}}""\"

    Si l'expediteur et l'objet ne suffisent pas, renvoie la catégorie "{TO_CLASSIFY}"

    Si tu as compris répond "{PROMPT_UNDERSTOOD}"
"""

MISTRAL_MAIL_NO_BODY_PROMPT = """
    Voici l'expéditeur du mail à catégoriser : ""\"{expediteur}""\"
    Voici l'objet du mail à catégoriser :  ""\"{objet}""\"
"""

class OllamaMistralPrompting:
    __HISTORY: list[Message] = [];

    @classmethod
    def ollama_mistral_chat(cls, content: str, *, add_to_history: bool = False, print_response: bool = False) -> str:
        """
        :return: the content of the returned message
        """
        message = {
            "role": "user",
            "content": content
        }

        if add_to_history:
            cls.__HISTORY.append(
                message
            )
            messages = cls.__HISTORY
        else:
            messages = cls.__HISTORY + [message]

        response = ollama.chat(
            model="mistral",
            messages=messages,
        )

        if add_to_history:
            cls.__HISTORY.append(response.message)

        if print_response:
            pprint(response)
        return response.message.content.strip()

    @classmethod
    def ollama_mistral_define_assistant(cls) -> bool:
        """
        :return: True if the assitant is correctly defined, else False
        """
        resp = cls.ollama_mistral_chat(MISTRAL_MAIL_MANAGER_PROMPT_NEVER_BODY, add_to_history=True)
        print(f"Defining assistant : '{resp}'")
        return resp == PROMPT_UNDERSTOOD

    @classmethod
    def ollama_getLabel(cls, expediteur, objet):
        """Fonction qui retorune un label à partir de l'objet et de l'expéditeur
        d'un mail grâce à l'API d'Ollama

        Args:
            expediteur (String): expediteur du mail
            objet (String): objet du mail
            mail (String): contenu du mail

        Returns:
            String : label associé à ce mail
        """
        if not expediteur:
            expediteur = "expéditeur non trouvé"
        if not objet:
            objet = "objet non trouvé"

        resp = cls.ollama_mistral_chat(
                MISTRAL_MAIL_NO_BODY_PROMPT.format(expediteur=expediteur, objet=objet)
            )

        return resp
