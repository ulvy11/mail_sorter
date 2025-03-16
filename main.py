from utils import ask_user_choice
from gmail_services import define_labels, set_labels, delete_promotions
from label_check import check_labels

def main():
    text_pre_choice = "Choose '1' to define, '2' to check labels, '3' to set labels, '4' to trash promotional mails"
    if (choice := ask_user_choice([str(i) for i in range(1,5)], text_pre_choice=text_pre_choice)) == '1':
        define_labels(max_page=1)
    elif choice == '2':
        check_labels()
    elif choice == '3':
        set_labels()
    elif choice == '4':
        delete_promotions()

if __name__ == "__main__":
    main()
