"""
books.py
Handles all book-related operations for the Library CLI system.
Fully title-based search. Uses the in-memory BOOKS dict in data_store.py.
"""

from data_store import (
    BOOKS,
    find_book_id_by_title,
    find_all_book_ids_by_title,
    find_books_by_partial_title,
    add_book,
    update_book_by_title,
    delete_book_by_title,
    get_book_by_title,
    borrow_book,
    return_book,
    list_books,
)

import validators

def highlight(word, text):
    """Highlight the matched word inside the title (case-insensitive)."""
    w = word.lower()
    t = text.lower()

    start = t.find(w)
    if start == -1:
        return text  # no highlight possible

    end = start + len(word)

    # Insert brackets or styling
    return text[:start] + "[" + text[start:end] + "]" + text[end:]


# -------------------------------------------------------------------
# ADD A BOOK
# -------------------------------------------------------------------
def add_new_book():
    #CLI function to add a new book using user input.

    book_id = input("Enter Book ID (e.g., B001): ").strip()
    if not validators.validate_book_id(book_id):
        print("❌ Invalid Book ID format!")
        return

    name = input("Enter Book Title: ").strip()
    if not validators.validate_book_title(name):
        print("❌ Invalid Book Title!")
        return

    author = input("Enter Author Name: ").strip()
    if not validators.validate_author(author):
        print("❌ Invalid Author!")
        return

    year = input("Enter Publication Year: ").strip()
    if not validators.validate_year(year):
        print("❌ Invalid Year!")
        return

    genre = input("Enter Genre: ").strip()
    if not validators.validate_genre(genre):
        print("❌ Invalid Genre!")
        return

    success = add_book(book_id, name, author, year, genre)

    if success:
        print("✅ Book added successfully!")
    else:
        print("❌ Book ID or Title already exists!")

# -------------------------------------------------------------------
# VIEW A BOOK
# -------------------------------------------------------------------

def view_book():
    print("\n--- Search Books ---")
    query = input("Enter part of the book title: ").strip()

    matches = find_all_book_ids_by_title(query)

    if not matches:
        print("❌ No books found.")
        return

    print(f"\n✔ Found {len(matches)} matching books:\n")

    for book_id in matches:
        book = BOOKS[book_id]

        # Highlight matched word in title
        highlighted_title = highlight(query, book["name"])

        print(f"ID: {book_id}")
        print(f"Title: {highlighted_title}")
        print(f"Author: {book['author']}")
        print(f"Year: {book['year']}")
        print(f"Genre: {book['genre']}")
        print(f"Available: {'Yes' if book['available'] else 'No'}")
        print("-" * 40)


# -------------------------------------------------------------------
# UPDATE A BOOK
# -------------------------------------------------------------------

def prompt_user_to_select_book(matches):
    if len(matches) == 0:
        print("No matching books found.")
        return None

    if len(matches) == 1:
        return matches[0]

    print(f"\nMultiple books match your search:\n")
    for idx, (bid, book) in enumerate(matches, start=1):
        print(f"{idx}. {book['name']} (ID: {bid})")

    while True:
        choice = input("\nEnter the number to select a book: ").strip()
        if not choice.isdigit():
            print("Enter a valid number.")
            continue

        choice = int(choice)
        if 1 <= choice <= len(matches):
            return matches[choice - 1]

        print("Invalid selection.")


def update_book():
    title = input("Enter book title to edit: ").strip()

    matches = find_books_by_partial_title(title)
    selected = prompt_user_to_select_book(matches)

    if not selected:
        return

    book_id, book = selected

    print(f"\nEditing book: {book['name']} (ID: {book_id})")
    print("Leave a field empty to keep current value.\n")

    new_title = input(f"New title ({book['name']}): ").strip() or book['name']
    new_author = input(f"New author ({book['author']}): ").strip() or book['author']
    new_year = input(f"New year ({book['year']}): ").strip() or book['year']
    new_genre = input(f"New genre ({book['genre']}): ").strip() or book['genre']

    success = update_book_by_title(
        original_title=book["name"],
        new_title=new_title,
        new_author=new_author,
        new_year=new_year,
        new_genre=new_genre
    )

    if success:
        print("\nBook updated successfully!\n")
    else:
        print("\nFailed to update the book.\n")




# -------------------------------------------------------------------
# DELETE A BOOK
# -------------------------------------------------------------------

def delete_book():
    print("\n--- Delete Book ---")
    query = input("Enter part of the book title to delete: ").strip()

    matches = find_all_book_ids_by_title(query)

    if not matches:
        print("❌ No books found.")
        return

    # If multiple, choose one
    if len(matches) > 1:
        print(f"\nMultiple books match '{query}':\n")
        for i, book_id in enumerate(matches, start=1):
            print(f"{i}. {BOOKS[book_id]['name']} (ID: {book_id})")

        choice = input("\nEnter the number to select a book: ").strip()

        if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
            print("❌ Invalid choice.")
            return

        book_id = matches[int(choice) - 1]

    else:
        book_id = matches[0]

    book = BOOKS[book_id]

    print("\n⚠ Are you sure you want to DELETE this book?")
    print(f" → {book['name']} (ID: {book_id})")

    confirm = input("Type YES to confirm: ").strip().lower()

    if confirm == "yes":
        BOOKS.pop(book_id)
        print("✔ Book deleted successfully!")
    else:
        print("❌ Deletion canceled.")



# -------------------------------------------------------------------
# BORROW / RETURN
# -------------------------------------------------------------------

def borrow_book_cli():
    print("\n--- Borrow a Book ---")
    title = input("Enter title of book to borrow: ").strip()

    matches = find_all_book_ids_by_title(title)

    if not matches:
        print("❌ No book found with that title.")
        return

    # If exactly one match, auto-select
    if len(matches) == 1:
        book_id = matches[0]
    else:
        # Show all matched books
        print("\nMultiple books found:")
        for i, bid in enumerate(matches, start=1):
            b = BOOKS[bid]
            print(f"{i}. {b['name']}  by {b['author']}  ({b['year']})  | ID: {bid}")

        # Ask user to pick
        while True:
            choice = input("Select book number: ")
            if choice.isdigit() and 1 <= int(choice) <= len(matches):
                book_id = matches[int(choice) - 1]
                break
            print("Invalid choice, try again.")

    # Now borrow using chosen book_id
    if not BOOKS[book_id]["available"]:
        print("❌ Book is already borrowed.")
        return

    BOOKS[book_id]["available"] = False
    print(f"✔ Borrowed: {BOOKS[book_id]['name']}")



def return_book_cli():
    print("\n--- Return a Book ---")
    title = input("Enter title of book to return: ").strip()

    matches = find_all_book_ids_by_title(title)

    if not matches:
        print("❌ No book found matching that title.")
        return

    # If only one match, auto-select
    if len(matches) == 1:
        book_id = matches[0]
    else:
        # Show all matched books
        print("\nMultiple books found:")
        for i, bid in enumerate(matches, start=1):
            b = BOOKS[bid]
            print(f"{i}. {b['name']} by {b['author']} ({b['year']}) | ID: {bid}")

        # Ask user to pick
        while True:
            choice = input("Select book number: ")
            if choice.isdigit() and 1 <= int(choice) <= len(matches):
                book_id = matches[int(choice) - 1]
                break
            print("Invalid choice, try again.")

    # Now attempt to return it
    if BOOKS[book_id]["available"]:
        print("❌ This book is already marked as returned.")
        return

    BOOKS[book_id]["available"] = True
    print(f"✔ Returned: {BOOKS[book_id]['name']}")



# -------------------------------------------------------------------
# LIST ALL BOOKS
# -------------------------------------------------------------------

def list_all_books():
    #Shows all books.
    db = list_books()

    if not db:
        print("📭 No books added yet.")
        return

    print("\n📚 ALL BOOKS")
    for book_id, data in db.items():
        print(f"\nID: {book_id}")
        print(f"Title: {data['name']}")
        print(f"Author: {data['author']}")
        print(f"Year: {data['year']}")
        print(f"Genre: {data['genre']}")
        print(f"Available: {'Yes' if data['available'] else 'No'}")