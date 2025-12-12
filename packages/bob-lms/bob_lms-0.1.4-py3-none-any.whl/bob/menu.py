'''
Welcome User!
1 = View all books
2 = Search book by title
3 = Borrow Book
4 = Return Book
5 = Logout

input(">>>")
>>>
'''

def user_menu():
    print("Welcome User!")
    from .auth import require_admin
    from . import books as b
    from . import validators as v
    from .auth import logout_flow
    from .books import borrow_book_cli, return_book_cli, list_all_books, view_book

    # Letting the user to put option
    while True:
        print("\nMENU:")
        print("1. View all books")
        print("2. Search book by title")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            list_all_books()
        elif choice == "2":
            view_book()
        elif choice == "3":
            borrow_book_cli()
        elif choice =="4":
            return_book_cli()
        elif choice == "5":
            logout_flow()
            break
        else:
            print("Invalid choice. Please try again") 