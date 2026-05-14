from flask import Flask, render_template, request, redirect
import mysql.connector
import random
import string

app = Flask(__name__)

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Muvvala@2007",
    database="url_shortner"
)

cursor = conn.cursor()

# Home Page
@app.route('/', methods=['GET', 'POST'])
def home():

    short_url = None

    if request.method == 'POST':

        original_url = request.form['long_url']

        # Generate short code
        short_code = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=6
            )
        )

        # Insert into database
        query = """
        INSERT INTO urls (original_url, short_code)
        VALUES (%s, %s)
        """

        values = (original_url, short_code)

        cursor.execute(query, values)

        conn.commit()

        short_url = f"http://127.0.0.1:5000/{short_code}"

    return render_template(
        'index.html',
        short_url=short_url
    )

# REDIRECTION FEATURE
@app.route('/<short_code>')
def redirect_url(short_code):

    query = """
    SELECT original_url
    FROM urls
    WHERE short_code = %s
    """

    cursor.execute(query, (short_code,))

    result = cursor.fetchone()

    if result:
        return redirect(result[0])

    return "URL Not Found"

if __name__ == '__main__':
    app.run(debug=True)