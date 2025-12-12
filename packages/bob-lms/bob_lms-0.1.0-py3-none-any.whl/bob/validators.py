"""
validators.py
Contains input validation utilities for the Library CLI system.
Keeps the system safe from invalid or malformed inputs.
"""


# -------------------------------------------------------------------
# BASIC VALIDATORS
# -------------------------------------------------------------------

def is_non_empty(text):
    #Check if a string is not empty after stripping spaces.
    return isinstance(text, str) and text.strip() != ""


def validate_year(year):
    #Validate that year is a number between 1000 and current decade.
    try:
        yr = int(year)
        return 1000 <= yr <= 2027
    except ValueError:
        return False


def validate_genre(genre):
    #Basic genre validation (non-empty).
    return is_non_empty(genre)


def validate_book_title(title):
    #Title must be non-empty and not too long.
    return is_non_empty(title) and len(title.strip()) <= 120


def validate_author(author):
    #Author must be non-empty.
    return is_non_empty(author)


# -------------------------------------------------------------------
# BOOK ID VALIDATION
# -------------------------------------------------------------------

def validate_book_id(book_id):
    """
    Book ID format check.
    Expected pattern: B001, B002, etc.
    """
    if not isinstance(book_id, str):
        return False

    book_id = book_id.strip()

    # Must start with B + digits
    if len(book_id) < 2 or not book_id.startswith("B"):
        return False

    digits = book_id[1:]
    return digits.isdigit()


# -------------------------------------------------------------------
# USER VALIDATION
# -------------------------------------------------------------------

def validate_username(username):
    #Usernames must be non-empty and not contain spaces.
    if not is_non_empty(username):
        return False
    return " " not in username


def validate_password(password):
    #Password must be at least 4 chars.
    return isinstance(password, str) and len(password) >= 4
