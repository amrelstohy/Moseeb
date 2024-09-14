from flask import Flask, render_template, request
from models import *
from models import storage
from flask_wtf import CSRFProtect
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 
csrf = CSRFProtect(app)

@app.route('/')
def home():
    items = storage.all('Item').values()
    ten_items = []
    count = 0
    for item in items:
        if count < 10 :
            ten_items.append(item)
            count = count + 1
        else:
            break
    print(str(storage.all('User')))
    return render_template('home.html', items=ten_items)

@app.route('/signin')
def SignIn():
    return render_template('signin/form.html')

@app.route('/submit', methods=['POST'])
def submit():
    from models.auth import Auth
    email = request.form['email']
    password = request.form['password']
    if Auth.SignIn(email, password) == 'email':
        return render_template('signin/form.html')
    return 'hi'
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)