def check_password(password):

    password_length = len(password)

    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)

    score = 0

    if password_length >= 8:
        score += 25

    if has_uppercase:
        score += 20

    if has_lowercase:
        score += 20

    if has_number:
        score += 20

    if has_special:
        score += 15

    if score >= 90:
        strength = "Very Strong 💪"
    elif score >= 70:
        strength = "Strong ✅"
    elif score >= 40:
        strength = "Medium ⚠️"
    else:
        strength = "Weak ❌"

    return {
        "length": password_length,
        "uppercase": has_uppercase,
        "lowercase": has_lowercase,
        "number": has_number,
        "special": has_special,
        "score": score,
        "strength": strength
    }

def check_common_password(password):
    """
    Check if the password exists in the common passwords database.
    Returns True if found, otherwise False.
    """

    try:
        with open("common_passwords.txt", "r") as file:
            common_passwords = file.read().splitlines()

        return password.lower() in [p.lower() for p in common_passwords]

    except FileNotFoundError:
        return False