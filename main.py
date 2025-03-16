from utils import ask_user_choice
from credentials_manager import CredentialsManager
from gmail_services import define_labels, set_labels
from label_check import check_labels

def main():
    if (choice := ask_user_choice(['1', '2', '3'], text_pre_choice="Choose '1' to define, '2' to check labels, '3' to set labels")) == '1':
        define_labels(CredentialsManager.get_creds(), max_page=1)
    elif choice == '2':
        check_labels()
    else:
        set_labels(CredentialsManager.get_creds())

if __name__ == "__main__":
    main()
