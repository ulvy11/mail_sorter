from typing import Any
from pickle import dump, load

LABEL = "label"
THREAD_ID = "threadId"
SENDER = "sender"
OBJECT = "object"
MAILS_LABELED_PICKLE_FILE = "mails_labeled.pck"


def register_pickle(obj: Any, file_path: str) -> None:
    with open(file_path, "wb") as pickle_file:
        dump(obj, pickle_file)


def get_pickle(file_path: str) -> Any:
    with open(file_path, "rb") as file:
        return load(file)


def ask_user_choice(options: list[str], *, text_pre_choice: str = None) -> str:
    if text_pre_choice is not None:
        print(text_pre_choice)
    while True:
        choice = input(f"Please choose an option ({" or ".join(options)}): ")
        if choice in options:
            return choice
        else:
            print(f"Invalid choice. Please enter {" or ".join(options)}.")


def ask_user_yn(text: str) -> bool:
    return ask_user_choice(["y", "n"], text_pre_choice=text) == "y"
