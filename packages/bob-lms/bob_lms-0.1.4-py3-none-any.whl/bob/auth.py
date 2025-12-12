from . import validators as v
from . import data_store as db


# -------------------------------------------------------------------
# LOGIN LOGIC
# -------------------------------------------------------------------

def login_flow():
    """
    Ask for username + password, validate them,
    login if correct, return True/False based on success.
    CLI modules will call this function.
    """
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    #input Validation
    if not v.validate_username(username):
        print("❌ Invalid Username!")
        return False
    
    if not v.validate_password(password):
        print("❌ Invalid Password!")
        return False

    #Credential Validation
    if not db.validate_user(username, password):
        print("❌ Incorrect Username or Password!")
        return False
    
    #Successful login
    db.login(username)
    print(f"✅ Logged in as {username}!")
    return True

# -------------------------------------------------------------------
# LOGOUT LOGIC
# -------------------------------------------------------------------
def logout_flow():
    """
    Logout the current user.
    CLI modules will call this function.
    """
    if not db.is_logged_in():
        print("❌ No user is currently logged in!")
        return False
    
    print(f"✅ User {db.get_current_user()} logged out successfully!")
    db.logout()
    print("✅ Logged out successfully!")
    return True

# -------------------------------------------------------------------
# AUTH GUARD
# -------------------------------------------------------------------
def require_login():
    """
    Check if a user is logged in.
    If not, print message and return False.
    If yes, return True.
    CLI modules will call this function before protected actions.
    """
    if not db.is_logged_in():
        print("❌ You must be logged in to perform this action!")
        return False
    return True


def require_admin():
    """
    Check if the current user is an admin.
    If not, print message and return False.
    If yes, return True.
    CLI modules will call this function before admin-only actions.
    """
    if not db.is_logged_in():
        print("❌ You must be logged in to perform this action!")
        return False
    
    username = db.get_current_user()
    role = db.get_user_role(username)

    if role != "admin":
        print("❌ You must be an admin to perform this action!")
        return False

    return True