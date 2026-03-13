import sqlite3
import random
import string
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

DATABASE = "urls.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute()

    conn.commit()
    conn.close()


def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.route("/", methods=["GET", "POST"])
def home():

    short_url = None

    if request.method == "POST":

        original_url = request.form["url"]

        short_code = generate_short_code()

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO urls(short, original) VALUES (?, ?)",
            (short_code, original_url)
        )

        conn.commit()
        conn.close()

        short_url = request.host_url + short_code

    return render_template("index.html", short_url=short_url)


@app.route("/<short_code>")
def redirect_url(short_code):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original FROM urls WHERE short=?",
        (short_code,)
    )

    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found"


if __name__ == "__main__":
    init_db()
    app.run(debug=True)