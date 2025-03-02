from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
import os
from datetime import timedelta  # Import for session timeout

app = Flask(__name__)
app.secret_key = "mysecretkey"  # Secret key for session management
app.permanent_session_lifetime = timedelta(minutes=30)  # Keep session active for 30 minutes

# File to store user data
users_file = "users.txt"

# Ensure users.txt exists
if not os.path.exists(users_file):
    open(users_file, "w").close()


# ✅ Home Page Route
@app.route('/')
def home():
    print("Session Data at Home:", session)  # Debugging print
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))  # Redirect to login if not logged in


# ✅ Registration Page Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        section = request.form['section']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match! <a href='/register'>Try Again</a>"

        # Save user details in a file (comma-separated)
        with open(users_file, "a") as file:
            file.write(f"{name},{department},{year},{section},{password}\n")

        return redirect(url_for('login'))  # Redirect to login page

    return render_template('register.html')


# ✅ Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        with open(users_file, "r") as file:
            users = file.readlines()
            for user in users:
                stored_name, _, _, _, stored_password = user.strip().split(',')
                if username == stored_name and password == stored_password:
                    session.permanent = True  # Keep session active
                    session['username'] = username  # Store username in session
                    print("Session Set:", session)  # Debugging print
                    return redirect(url_for('home'))  # Redirect to home page

        return "Invalid username or password! <a href='/login'>Try Again</a>"

    return render_template('login.html')


# ✅ Logout Route (Now Supports GET & POST)
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('exit_page'))  # Redirect to exit page


# ✅ Exit Page Route
@app.route('/exit')
def exit_page():
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(debug=True)
