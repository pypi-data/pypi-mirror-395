

from .auth import require_admin, logout_flow
from .books import *
from . import validators as v
from . import data_store as bb

# -------------------------------------------------------------------
# ADMIN FUNCTIONS
# -------------------------------------------------------------------
def admin_menu():
    print("\n=== Admin Dashboard ===")
    print("Welcome, Admin!\n")

    while True:
        print("\n\nWhat do you want to do?")
        print("1 Add book")
        print("2 View all books")
        print("3 Search book by title")
        print("4 Edit books")
        print("5 Delete book")
        print("6 logout")

        choice=input(">>> ")

        if choice == "1":
            add_new_book()
     
        elif choice == "2":
            list_all_books()

        elif choice == "3":
            view_book()

        elif choice == "4":
            update_book()

        elif choice == "5":
            delete_book()
        
        elif choice == "6":
            logout_flow()
            break
        else:
            print("Invalid option! Try again.")       