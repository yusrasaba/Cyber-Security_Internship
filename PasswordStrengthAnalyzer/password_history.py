import hashlib


def hash_password(password):
    """
    Convert password into SHA-256 hash.
    """

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def is_password_reused(password):

    password_hash = hash_password(password)

    try:

        with open("password_history.txt", "r") as file:

            history = file.read().splitlines()

        return password_hash in history

    except FileNotFoundError:

        return False

def save_password(password):

    password_hash = hash_password(password)

    with open("password_history.txt", "a") as file:

        file.write(password_hash + "\n")