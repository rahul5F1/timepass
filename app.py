from flask import Flask, render_template, request, redirect, flash, session, jsonify 
from pymongo import MongoClient 
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
    question = request.form.get('security_question') 
    answer = request.form.get('security_answer')
    if password != confirm_password:
        flash("Passwords do not match!")
        return redirect('/') 
    if users_collection.find_one({"email": email}):    
        flash("Email already exists. Please login.")
        return redirect('/') 
    users_collection.insert_one({    
        "name": name,    
        "email": email,    
        "password": password,    
        "security_question": question,    
        "security_answer": answer }) 
    flash("Registration successful. Please login.") 
    return redirect('/')

@app.route('/login', methods=['POST']) 
def login(): 
    email = request.form.get('email') 
    password = request.form.get('password') 
    user = users_collection.find_one({"email": email, "password": password})
    if user:    
        session['user_id'] = str(user['_id'])    
        session['user_name'] = user['name']    
        return redirect('/dashboard') 
    else:    
        flash("Invalid credentials. Please try again.")    
        return redirect('/')

@app.route('/verify_data', methods=['POST'])
def verify_data():
   if request.is_json:
       try:
           data = request.get_json()
           v_email = data.get('email')
           v_question = data.get('question')
           v_answer = data.get('answer')
           if users_collection.find_one({"email":v_email,"security_question":v_question,"security_answer":v_answer}):
               verification_successful = True
               message = "Verification successful."
           else:
               verification_successful = False
               message = "Verification failed: Invalid credentials."

           response = {
               'success': verification_successful,
               'message': message
           }
           return jsonify(response), 200
       except Exception as e:
           return jsonify({'error': 'Failed to process JSON data', 'details': str(e)}), 400
   else:
       return jsonify({'error': 'Request body is not in JSON format'}), 400

@app.route('/reset_password', methods=['GET','POST']) 
def reset_password(): 
    data=request.get_json()
    email = data.get('email') 
    # question = data.get('security_question') 
    # answer = data.get('security_answer') 
    new_password = data.get('newPass') 
    # confirm_password = data.get('confirm_password')
    print(email)
    user = users_collection.find_one({"email": email}) 
    if not user:    
        return jsonify({"status": "error", "message": "Invalid question or answer."}) 
    # if new_password != confirm_password:    
    #     return jsonify({"status": "error", "message": "Passwords do not match."}) 
    users_collection.update_one({"_id": user['_id']}, {"$set": {"password": new_password}}) 
    return jsonify({"status": "success", "message": "Password reset successful."})

@app.route('/dashboard') 
def dashboard(): 
    if 'user_id' not in session: 
        return redirect('/') 
    return render_template('dashboard.html', name=session.get('user_name', 'User'))

@app.route('/logout') 
def logout(): 
    session.clear() 
    return redirect('/')

if __name__ == '__main__': 
    app.run(debug=True)
