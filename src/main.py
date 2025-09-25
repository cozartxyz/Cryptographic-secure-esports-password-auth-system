from auth.register import register_user
from auth.login import login_user
from utils.db import initialize_database


def display_menu():
    print("\n" + "=" * 40)
    print("         Welcome to EsportsAuth System         ")
    print("=" * 40)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("=" * 40)


def main():
    initialize_database()

    while True:
        display_menu()
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            print("\n" + "-" * 40)
            print("              Register User               ")
            print("-" * 40)
            register_user()
        elif choice == "2":
            print("\n" + "-" * 40)
            print("               Login User                 ")
            print("-" * 40)
            login_user()
        elif choice == "3":
            print("\n" + "=" * 40)
            print("         Thank you for using EsportsAuth       ")
            print("                 Goodbye!                 ")
            print("=" * 40)
            break
        else:
            print("\n" + "!" * 40)
            print("  Invalid option. Please try again!       ")
            print("!" * 40)


if __name__ == "__main__":
    main()
