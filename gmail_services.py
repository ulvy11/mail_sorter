from credentials_manager import CredentialsManager
from utils import *
from ollama_mistral_prompting import OllamaMistralPrompting

import os.path

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def get_ids_in_inbox_without_user_labels(service, *, max_page: int = None):
    """
    Returns:
        Table : [{"id" : id, "threadId" : threadId, "label": ""}, ...]
        For mails in inbox without userlabels
    """
    return get_mails_from_query(service, "in:inbox -has:userlabels", max_page=max_page)


def getObjetExpediteur(service, mailID):
    """Fonction qui retourne l'objet et l'expediteur d'un mail en fonction de l'id d'un
    mail avec l'API de gmail

    Args:
        service ():
        mailID (String): ID du mail dans l'API Gmail

    Returns:
        Table: [objet, expediteur]
    """
    msg = (
        service.users()
        .messages()
        .get(userId="me", id=mailID, format="metadata")
        .execute()
    )
    headers = msg.get("payload", {}).get("headers", [])

    expediteur = None
    objet = None

    for header in headers:
        if header.get("name") == "From":
            expediteur = header.get("value")
        elif header.get("name") == "Subject":
            objet = header.get("value")

    return [objet, expediteur]


def get_or_create_label(service, label_name):
    """Check if a label exists, and create it if it doesn't."""
    try:
        # List all labels
        labels = service.users().labels().list(userId="me").execute()
        for label in labels.get("labels", []):
            if label["name"] == label_name:
                return label["id"]  # Return existing label ID

        # Create the label if it doesn't exist
        label_body = {
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show",
        }
        new_label = (
            service.users().labels().create(userId="me", body=label_body).execute()
        )
        return new_label["id"]  # Return newly created label ID
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def define_labels(*, max_page: int = None) -> list[dict[str, str]]:
    mails_labeled: list[dict[str, str]] = []
    labels: dict[str, int] = {}
    # Setup Ollama
    if not OllamaMistralPrompting.ollama_mistral_define_assistant():
        print("Assistant badly defined")
        return

    try:
        service = build("gmail", "v1", credentials=CredentialsManager.get_creds())
        data = get_ids_in_inbox_without_user_labels(service, max_page=max_page)
        i = 0
        tailleTotale = len(data)
        for mail in data:
            i += 1
            objet, expediteur = getObjetExpediteur(service, mail["id"])
            print(f"{i}/{tailleTotale} - {expediteur} + {objet}", end=" ")

            label = OllamaMistralPrompting.ollama_getLabel(expediteur, objet)

            # removing quotes if any
            while (label.endswith('"') or label.endswith("'")) and (
                label.startswith('"') or label.endswith("'")
            ):
                label = label[1:-1]

            if label in labels.keys():
                labels[label] += 1
            else:
                labels[label] = 1

            mail[LABEL] = label
            mail_labeled = {
                "id": mail["id"],
                THREAD_ID: mail[THREAD_ID],
                LABEL: label,
                OBJECT: objet,
                SENDER: expediteur,
            }
            print(f"[{label}]")
            print()
            mails_labeled.append(mail_labeled)
    except HttpError as error:
        print(f"An error occurred: {error}")

    print(f"\nLabels generated ({len(labels)})")
    for label, count in labels.items():
        print(f"\t- {label} ({count})")

    register_pickle(mails_labeled, MAILS_LABELED_PICKLE_FILE)
    return mails_labeled


def set_labels() -> None:
    mails_labeled = get_pickle(MAILS_LABELED_PICKLE_FILE)
    labels_ids: dict[str, tuple[str, int]] = {}
    try:
        service = build("gmail", "v1", credentials=CredentialsManager.get_creds())
        i = 0
        tailleTotale = len(mails_labeled)
        for mail_labeled in mails_labeled:
            i += 1
            msg_id = mail_labeled["id"]
            label = mail_labeled[LABEL]
            print(
                f"{i}/{tailleTotale} - {mail_labeled[SENDER]} - {mail_labeled[OBJECT]} [{label}]"
            )
            if label in labels_ids.keys():
                label_id = labels_ids[label][0]
                labels_ids[label][1] += 1
            else:
                label_id = get_or_create_label(service, label)
                labels_ids[label] = [label_id, 1]
            service.users().messages().modify(
                userId="me",
                id=msg_id,
                body={"removeLabelIds": ["INBOX"], "addLabelIds": [label_id]},
            ).execute()
        print(f"\nUsed labels ({len(labels_ids)}):")
        for label, value in labels_ids.items():
            print(f"\t- {label} ({value[1]})")
        os.remove(MAILS_LABELED_PICKLE_FILE)

    except HttpError as error:
        print(f"An error occurred: {error}")


def get_mails_from_query(
    service, query: str, *, max_page: int = None
) -> list[dict[str, str]]:
    """
    Returns:
        List of dict with id and threadId
    """

    def is_max_page(curr_page: int):
        return max_page is not None and curr_page >= max_page

    mails = []
    page_index = 0
    print(f"Page {page_index}")
    results = service.users().messages().list(userId="me", q=query).execute()

    mails.extend(
        {"id": msg["id"], THREAD_ID: msg[THREAD_ID]} for msg in results["messages"]
    )

    while "nextPageToken" in results and not is_max_page(page_index):
        page_index += 1
        print(f"Page {page_index}")
        results = (
            service.users()
            .messages()
            .list(userId="me", pageToken=results["nextPageToken"])
            .execute()
        )
        mails.extend(
            {"id": msg["id"], THREAD_ID: msg[THREAD_ID]} for msg in results["messages"]
        )

    return mails


def delete_promotions() -> None:
    try:
        service = build("gmail", "v1", credentials=CredentialsManager.get_creds())
        # Search for messages in the Promotions category
        messages = get_mails_from_query(service, "category:promotions -has:userlabels")

        # If there are no messages, return
        if not messages:
            print("No promotional emails found.")
            return

        # Delete messages in batches
        for message in messages:
            service.users().messages().trash(userId="me", id=message["id"]).execute()

        print(f"Successfully deleted {len(messages)} promotional emails.")

    except HttpError as error:
        print(f"An error occurred: {error}")
