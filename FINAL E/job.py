from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secret key for session security

# In-memory storage for user profiles (replace this with a database in a real application)
user_profiles = {
    'user1': {'password': 'pass1', 'team': 'Mount Holyoke', 'email': 'user1@example.com'},
    'user2': {'password': 'pass2', 'team': 'Gayaza Girls', 'email': 'user2@example.com'},
}

@app.route('/')
def home():
    if 'username' in session:
        return f'Hello, {session["username"]} from Team {user_profiles[session["username"]]["team"]}! <a href="/logout">Logout</a>'
    return 'You are not logged in. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_profiles and user_profiles[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    team = user_profiles[session['username']]['team']
    return render_template('chat.html', username=session['username'], team=team)

if __name__ == '__main__':
    app.run(debug=True)
