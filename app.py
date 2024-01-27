from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sAtya@2003'
app.config['MYSQL_DB'] = 'user_db'

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Get form data
            id=requst.form['id']
            eamil=request.form['email']
            username = request.form['username']
            password = request.form['password']

            # Store data in the database
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('login'))
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            # Get form data
            username = request.form['username']
            password = request.form['password']

            # Check if user exists in the database (Note: In a real-world scenario, use password hashing)
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cur.fetchone()
            cur.close()

            if user:
                # Authentication successful
                return "Login successful!"
            else:
                # Authentication failed
                return "Invalid credentials. Please try again."
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('login.html')
