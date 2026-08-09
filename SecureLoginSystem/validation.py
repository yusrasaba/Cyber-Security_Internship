import re


def validate_username(username):
    if not username:
        return False, "Username is required."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if len(username) > 30:
        return False, "Username must not exceed 30 characters."

    if not re.fullmatch(r"[A-Za-z0-9_]+", username):
        return False, "Username can contain only letters, numbers, and underscores."

    return True, ""


def validate_email(email):
    if not email:
        return False, "Email is required."

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(pattern, email):
        return False, "Please enter a valid email address."

    return True, ""


def validate_password(password):
    if not password:
        return False, "Password is required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain a number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+]", password):
        return False, "Password must contain a special character."

    return True, ""