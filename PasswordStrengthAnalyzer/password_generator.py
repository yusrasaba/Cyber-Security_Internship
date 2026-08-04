import random
import string


def generate_password(length=12):
    """
    Generate a strong random password.
    """

    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*")

    remaining = ''.join(
        random.choice(
            string.ascii_letters +
            string.digits +
            "!@#$%^&*"
        )
        for _ in range(length - 4)
    )

    password = uppercase + lowercase + digit + special + remaining

    password_list = list(password)
    random.shuffle(password_list)

    return ''.join(password_list)