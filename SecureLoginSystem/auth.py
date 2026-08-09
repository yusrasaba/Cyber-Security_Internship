import bcrypt

from db import get_connection


def hash_password(password):
    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def register_user(username, email, password):

    password_hash = hash_password(password)

    connection = get_connection()

    try:

        connection.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, password_hash)
        )

        connection.commit()

        return True, "Registration successful."

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):
            return False, "Username or email already exists."

        return False, "Registration failed."

    finally:
        connection.close()


def authenticate_user(username, password):

    connection = get_connection()

    try:

        user = connection.execute(
            """
            SELECT id, username, email, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        if user is None:
            return None

        password_bytes = password.encode("utf-8")
        stored_hash = user["password_hash"].encode("utf-8")

        if bcrypt.checkpw(password_bytes, stored_hash):
            return user

        return None

    finally:
        connection.close()