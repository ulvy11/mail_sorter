from utils import ask_user_choice, MAILS_LABELED_PICKLE_FILE
from gmail_services import define_labels, set_labels
from label_check import check_labels

from sys import argv
from os.path import exists

CHOICES = {
    1: "to generate labels",
    2: "to check labels",
    3: "to set labels",
    4: "to do 1, 2, and 3",
}

CHOICES_NOT_NEEDING_PICKLE_FILE = [1]


def main():
    max_page = int(argv[1]) if len(argv) >= 2 else 1
    if max_page <= 0:
        return
    # remove one since it is an index
    max_page -= 1

    choices = (
        CHOICES
        if exists(MAILS_LABELED_PICKLE_FILE)
        else {i: CHOICES[i] for i in CHOICES_NOT_NEEDING_PICKLE_FILE}
    )

    text_pre_choice = "Type :" + "\n\t".join(
        [""] + [f"{key} - {value}" for key, value in choices.items()]
    )
    if (
        choice := ask_user_choice(
            [str(i) for i in choices.keys()], text_pre_choice=text_pre_choice
        )
    ) == "1":
        define_labels(max_page=max_page)
    elif choice == "2":
        check_labels()
    elif choice == "3":
        set_labels()
    elif choice == "4":
        define_labels(max_page=max_page)
        print()
        check_labels()
        print()
        set_labels()


if __name__ == "__main__":
    main()
