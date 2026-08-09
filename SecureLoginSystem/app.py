import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from db import initialize_database

from auth import (
    register_user,
    authenticate_user
)

from validation import (
    validate_username,
    validate_email,
    validate_password
)


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY"
)

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "FLASK_SECRET_KEY environment variable is not set."
    )

# Session security settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"


initialize_database()


@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return """
        <h1>Secure Login System</h1>

        <p>
            <a href="/register">Register</a>
        </p>

        <p>
            <a href="/login">Login</a>
        </p>
    """


@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # Validate username
        valid, message = validate_username(username)

        if not valid:

            return render_template(
                "register.html",
                message=message
            )

        # Validate email
        valid, message = validate_email(email)

        if not valid:

            return render_template(
                "register.html",
                message=message
            )

        # Validate password
        valid, message = validate_password(password)

        if not valid:

            return render_template(
                "register.html",
                message=message
            )

        # Confirm password
        if password != confirm_password:

            return render_template(
                "register.html",
                message="Passwords do not match."
            )

        # Register user
        success, message = register_user(
            username,
            email,
            password
        )

        return render_template(
            "register.html",
            message=message
        )

    return render_template(
        "register.html",
        message=message
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = authenticate_user(
            username,
            password
        )

        if user:

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("dashboard")
            )

        message = "Invalid username or password."

    return render_template(
        "login.html",
        message=message
    )


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":
    app.run(debug=True)