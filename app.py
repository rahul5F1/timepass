from flask import Flask, render_template, request, redirect, flash, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['project']
users_collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Check if the passwords match
    if password != confirm_password:
        flash("Passwords do not match!")
        return redirect('/')

    # Check if email already exists in database
    if users_collection.find_one({"email": email}):
        flash("Email already exists. Please login.")
        return redirect('/')

    # Insert user data into MongoDB
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": password  # NOTE: Hash the password in production!
    })
    flash("Registration successful. Please login.")
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the email and password exist in the database
    user = users_collection.find_one({"email": email, "password": password})
    if user:
        # Store user information in session after successful login
        session['user_id'] = str(user['_id'])
        session['user_name'] = user['name']
        return redirect('/dashboard')
    else:
        flash("Invalid credentials. Please try again.")
        return redirect('/')

@app.route('/dashboard')
def dashboard():
    # Ensure the user is logged in
    if 'user_id' not in session:
        return redirect('/')
    
    # Fetch user data based on session
    user_name = session.get('user_name', 'User')
    return render_template('dashboard.html', name=user_name)

@app.route('/logout')
def logout():
    # Clear the session and redirect to login page
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
