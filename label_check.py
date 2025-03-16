from utils import *
from label_rules import EXPECTED_LABELS, TO_CLASSIFY, TRANSFORMATION_RULES

def check_labels() -> None:
    mails_labeled = get_pickle(MAILS_LABELED_PICKLE_FILE)
    for mail_labeled in mails_labeled:
        label: str = mail_labeled[LABEL]
        if label in TRANSFORMATION_RULES.keys():
            mail_labeled[LABEL] = TRANSFORMATION_RULES[label]
        elif label not in EXPECTED_LABELS:
            print(label)
            if ask_user_yn(f"change to {TO_CLASSIFY}?"):
                mail_labeled[LABEL] = TO_CLASSIFY
            else:
                new_label_found = False
                while not new_label_found:
                    new_label = input("Choose another label:")
                    if new_label_found := ask_user_yn(f"new label : '{new_label}'"):
                        mail_labeled[LABEL] = new_label

    register_pickle(mails_labeled, MAILS_LABELED_PICKLE_FILE)
