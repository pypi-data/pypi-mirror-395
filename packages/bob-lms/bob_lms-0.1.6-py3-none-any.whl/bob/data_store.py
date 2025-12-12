# -------------------------------------------------------------------
# SECTION 1: IN-MEMORY DATABASES
# -------------------------------------------------------------------

from .validators import *
"""
Book Format:
"B001": {
        "name": "",
        "author": "",
        "year": "",
        "genre": "",
        "available": True,
    },
"""


BOOKS = {
    "B001": {
        "name": "H.C. Verma Concepts of Physics Vol. 1 & 2",
        "author": "H.C. Verma",
        "year": "2024",
        "genre": "Educational Textbooks",
        "available": True,
    },
    "B002": {
        "name": "D.C. Pandey Understanding Physics series",
        "author": "D.C. Pandey",
        "year": "2013",
        "genre": "Educational Textbooks",
        "available": True,
    },
    "B003": {
        "name": "I.E. Irodov Problems in General Physics",
        "author": "I.E. Irodov",
        "year": "2023",
        "genre": "Educational Textbooks",
        "available": True,
    },
    "B004": {
        "name": "Problems in Physical Chemistry ",
        "author": "Narendra Avasthi",
        "year": "2010",
        "genre": "Educational Textbooks",
        "available": True,
    },
    "B005": {
        "name": "Advanced Problems in Organic Chemistry",
        "author": "M.S. Chauhan",
        "year": "2025",
        "genre": "Educational Textbooks",
        "available": True,
    },
    "B006": {
        "name": "Higher Algebra",
        "author": "Hall & Knight",
        "year": "",
        "genre": "Educational Textbooks",
        "available": True,
    },
    "B007": {
        "name": "Advanced Problems in Mathematics for JEE Main & Advanced",
        "author": "Vikas Gupta",
        "year": "2025",
        "genre": "Educational Textbooks",
        "available": True,
    },
    
    "B008": {
        "name": "Differential & Integral Calculus",
        "author": "Amit M. Agarwal",
        "year": "2017",
        "genre": "Educational Textbooks",
        "available": True,
    },
    
    "B009": {
        "name": "Cengage",
        "author": "G. Tewani",
        "year": "2025",
        "genre": "Educational Textbooks",
        "available": True,
    },
    
    "B010": {
        "name": "Game of Thrones",
        "author": "George R.R. Martin",
        "year": "1996",
        "genre": "Fantasy",
        "available": True,
    },

    "B011": {
        "name": "A Clash of Kings",
        "author": "George R.R. Martin",
        "year": "1999",
        "genre": "Fantasy",
        "available": True,
    },

    "B012": {
        "name": "A Storm of Swords",
        "author": "George R.R. Martin",
        "year": "2000",
        "genre": "Fantasy",
        "available": True,
    },

    "B013": {
        "name": "A Feast for Crows",
        "author": "George R.R. Martin",
        "year": " 2005",
        "genre": "Fantasy",
        "available": True,
    },

    "B014": {
        "name": "A Dance with Dragons",
        "author": "George R.R. Martin",
        "year": "2011",
        "genre": "Fantasy",
        "available": True,
    },

    "B015": {
        "name": "American Prometheus: The Triumph and Tragedy of J. Robert Oppenheimer",
        "author": "Kai Bird and Martin J. Sherwin",
        "year": "2005",
        "genre": "History",
        "available": True,
    },

    "B016": {
        "name": "The Great Gatsby",
        "author": " F. Scott Fitzgerald",
        "year": "1925",
        "genre": "Tragedy",
        "available": True,
    },

    "B017": {
        "name": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "year": "1997",
        "genre": "Adventure and Fantasy",
        "available": True,
    },

    "B018": {
        "name": "Harry Potter and the Deathly Hallows",
        "author": "J.K. Rowling",
        "year": "",
        "genre": "Adventure and Fantasy",
        "available": True,
    },

    "B019": {
        "name": "Harry Potter and the Half-Blood Prince",
        "author": "J.K. Rowling",
        "year": "2000",
        "genre": "Adventure and Fantasy",
        "available": True,
    },

    "B020": {
        "name": "Harry Potter and the Order of the Phoenix",
        "author": "J.K. Rowling",
        "year": "2003",
        "genre": "Adventure and Fantasy",
        "available": True,
    },

    "B021": {
        "name": "Geronimo Stilton: The Kingdom of Fantasy",
        "author": "Elisabetta Dami",
        "year": "2009 ",
        "genre": "Children's Fantasy, Adventure",
        "available": True,
    },

    "B022": {
        "name": "Count of Monte Cristo",
        "author": "Alexandre Dumas ",
        "year": "1846",
        "genre": "Historical Novel, Adventure",
        "available": True,
    },

    "B023": {
        "name": "Around the world in 80 days",
        "author": "Jules Verne",
        "year": "1872",
        "genre": "Adventure, Science Fiction",
        "available": True,
    },

    "B024": {
        "name": "Tale of Two Cities",
        "author": "Charles Dickens",
        "year": "1859",
        "genre": "Historical Fiction, Classic Literature",
        "available": True,
    },

    "B025": {
        "name": "Diary of a Wimpy Kid",
        "author": "Jeff Kinney",
        "year": "2007",
        "genre": "Children's Fiction, Humor, Graphic Novel",
        "available": True,
    },
}


"""
User format:
"admin": {
        "password": "pass",
        "role": "admim/user",
    }
"""


USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
    },
    "user1": {
        "password": "useronepass",
        "role": "user",
    },
}


current_user = None

# -------------------------------------------------------------------
# SECTION 2: BOOK TITLE SEARCH UTILITIES
# -------------------------------------------------------------------

def normalize_title(title):
    #Normalize book titles for case-insensitive searching.
    return title.strip().lower()


def find_book_id_by_title(title):
    #Return the book_id for the book matching a given title.
    search_title = normalize_title(title)

    for book_id, data in BOOKS.items():
        book_title = normalize_title(data["name"])
        if search_title in book_title:
            return book_id

    return None

# -------------------------------------------------------------------
# SECTION 3: BOOK OPERATIONS (TITLE-BASED)
# -------------------------------------------------------------------

def add_book(book_id, title, author, year, genre):
    #Create a new book using book ID.
    if book_id in BOOKS:
        return False  # ID already taken

    # Also ensure no duplicate title exists
    if find_book_id_by_title(title):
        return False  # Book with same title exists

    BOOKS[book_id] = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "available": True
    }
    return True


def get_book_by_title(title):
    #Return a book dict using only the title.
    book_id = find_book_id_by_title(title)
    if not book_id:
        return None
    return BOOKS[book_id]


def find_all_book_ids_by_title(title):
    """
    Return a list of all book_ids where the title contains the search string.
    Case-insensitive partial match.
    """
    search_title = normalize_title(title)
    matches = []

    for book_id, data in BOOKS.items():
        if search_title in normalize_title(data["name"]):
            matches.append(book_id)

    return matches


def find_books_by_partial_title(search_term):
    """Return list of (book_id, book_dict) where title contains the search term."""
    term = search_term.lower()
    matches = []

    for book_id, data in BOOKS.items():
        if term in data["name"].lower():
            matches.append((book_id, data))

    return matches


def update_book_by_title(original_title, new_title=None, new_author=None, new_year=None, new_genre=None):
    """Update a book using its title (case insensitive exact match)."""

    original_title_normalized = normalize_title(original_title)

    # Find the book_id by exact title match after normalization
    book_id = None
    for bid, data in BOOKS.items():
        if normalize_title(data["name"]) == original_title_normalized:
            book_id = bid
            break

    if not book_id:
        return False  # No book found

    # Update fields ONLY if valid and provided
    if new_title and validate_book_title(new_title):
        BOOKS[book_id]["name"] = new_title

    if new_author and validate_author(new_author):
        BOOKS[book_id]["author"] = new_author

    if new_year and validate_year(new_year):
        BOOKS[book_id]["year"] = int(new_year)

    if new_genre and validate_genre(new_genre):
        BOOKS[book_id]["genre"] = new_genre

    return True



def delete_book_by_title(title):
    #Delete a book from the DB using only title.
    book_id = find_book_id_by_title(title)
    if not book_id:
        return False
    BOOKS.pop(book_id)
    return True


def list_books():
    #Return full books DB.
    return BOOKS


# -------------------------------------------------------------------
# SECTION 4: BORROWING & RETURNING
# -------------------------------------------------------------------

def borrow_book(title):
    """Mark book as borrowed."""
    book_id = find_book_id_by_title(title)
    if not book_id:
        return False

    if not book_id:
        return False

    BOOKS[book_id]["available"] = False
    return True


def return_book(title):
    """Mark book as returned."""
    book_id = find_book_id_by_title(title)
    if not book_id:
        return False

    BOOKS[book_id]["available"] = True
    return True


# -------------------------------------------------------------------
# SECTION 5: USER OPERATIONS
# -------------------------------------------------------------------

def add_user(username, password, role="user"):
    #Register a new user.
    if username in USERS:
        return False

    USERS[username] = {
        "password": password,
        "role": role
    },
    return True


def validate_user(username, password):
    #Check username + password pair.
    usr = USERS.get(username)
    if not usr:
        return False
    return usr["password"] == password


def get_user_role(username):
    #Return the role of a given user.
    usr = USERS.get(username)
    if not usr:
        return None
    return usr["role"]


# -------------------------------------------------------------------
# SECTION 6: SESSION MANAGEMENT
# -------------------------------------------------------------------

def login(username):
    #Set current logged in user.
    global current_user
    current_user = username


def logout():
    #Logout currently active user.
    global current_user
    current_user = None


def get_current_user():
    return current_user


def is_logged_in():
    return current_user is not None


