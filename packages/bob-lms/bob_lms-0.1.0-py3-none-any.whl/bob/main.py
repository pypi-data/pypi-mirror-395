import time
from data_store import validate_user, get_user_role, login, logout
from menu import user_menu
from admin import admin_menu

def main():
    print("=== Welcome To B.O.B ===\n")
    print('''
██████╗░░░░░█████╗░░░░██████╗░░░░
██╔══██╗░░░██╔══██╗░░░██╔══██╗░░░
██████╦╝░░░██║░░██║░░░██████╦╝░░░
██╔══██╗░░░██║░░██║░░░██╔══██╗░░░
██████╦╝██╗╚█████╔╝██╗██████╦╝██╗
╚═════╝░╚═╝░╚════╝░╚═╝╚═════╝░╚═╝
🅱🅾🅾🅺🆂 🅾🅽 🅱🅾🅰🆁🅳 - Ⓑⓡⓞⓦⓢⓔ ⓐⓝⓓ Ⓑⓞⓡⓡⓞⓦ
===============================
Your Library Management System
===============================
    ''')

    while True:
        print("\nSelect an option:")
        print("1. Login")
        print("2. Exit")

        choice = input(">>> ").strip()

        if choice == "1":
            username = input("\nUsername: ").strip()
            password = input("Password: ").strip()

            if validate_user(username, password):
                login(username)
                role = get_user_role(username)
                print(f"\n✅ Logged in as: {username} ({role})\n")

                if role == "admin":
                    admin_menu()
                else:
                    user_menu()

                logout()
                print("\nLogged out successfully.\n")

            else:
                print("❌ Invalid username or password. Try again.\n")

        elif choice == "2":
            print("\nThank you for using B.O.B. Goodbye!\n")
            time.sleep(3)
            break

        else:
            print("❌ Invalid option. Please choose 1 or 2.\n")
