from flask import Flask, render_template, request, session, url_for, redirect
from models import *
from models import storage
from flask_wtf import CSRFProtect
import secrets
from models.auth import Auth


app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 
csrf = CSRFProtect(app)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    user_id = session.get('user_id')
    user = storage.all('User').get(user_id)
    items = storage.all('Item').values()
    ten_items = []
    count = 0
    for item in items:
        if count < 10 :
            ten_items.append(item)
            count = count + 1
        else:
            break
    return render_template('home.html', items=ten_items, user=user)

@app.route('/signin')
def SignIn():
    return render_template('signin/form.html')

@app.route('/signin/submit', methods=['POST'])
def SignInSubmit():
    email = request.form['email']
    password = request.form['password']
    auth = Auth.SignIn(email, password)
    if auth == 'email':
        email_error = 'This Email does not exist.'
        return render_template('signin/form.html', email=email, password=password, email_error=email_error )
    elif auth == 'password':
        password_error = 'error password'
        return render_template('signin/form.html', email=email, password=password, password_error=password_error )
    else:
        session['user_id'] = auth

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect(url_for('home'))


@app.route('/profile')
def profile():
    user = storage.all('User').get(session.get('user_id'))
    if user:
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('SignIn'))
    

@app.route('/signup')
def SignUp():
    return render_template('signup/form.html')

@app.route('/signup/submit', methods=['POST'])
def SignUpSubmit():
    print(request.form)
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    phone = request.form['phone']
    pwd = request.form['pwd']
    gender = request.form.get('gender')

    if not (fname and lname and email and phone and pwd):
        error_msg = 'please complete all required fields'
        return render_template('signup/form.html', fname=fname, lname=lname,
                               email=email, phone=phone, error_msg=error_msg)
    user_id = Auth.SignUp(fname, lname, email, phone, pwd, gender)
    if not user_id:
        error_msg = 'this email exists before.'
        return render_template('signup/form.html', fname=fname, lname=lname,
                               email=email, phone=phone, error_msg=error_msg)
    
    session['user_id'] = user_id
    return redirect(url_for('home'))


 
@app.route('/profile/update')
def UpdateProfile():
    user_id = session.get('user_id')
    if user_id:
        user = storage.all('User').get(user_id)
        fname = user.first_name
        lname = user.last_name
        phone = user.phone
        return render_template('update.html', fname=fname, lname=lname, phone=phone)
    else:
        return redirect(url_for('SignIn'))
    
@app.route('/profile/update/submit', methods=['POST'] )
def UpdateSubmit():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')

    if not (fname and lname and phone):
        error_msg = 'please complete all required fields'
        return render_template('update.html', fname=fname, lname=lname, phone=phone, error_msg=error_msg)
    else:
        user_id = session.get('user_id')
        user = storage.all('User').get(user_id)
        user.first_name = fname
        user.last_name = lname
        user.phone = phone
        storage.save()
        return redirect(url_for('profile'))
    

@app.route('/profile/resetpassword')
def ResetPassword():
    user_id = session.get('user_id')
    if user_id:
        return render_template('resetpassword.html')
    else:
        return redirect(url_for('SignIn'))
    

@app.route('/profile/resetpassword/submit', methods=['POST'])
def ResetPasswordSubmit():
    old_pwd = request.form.get('old_pwd')
    new_pwd = request.form.get('new_pwd')
    user_id = session.get('user_id')
    user = storage.all('User').get(user_id)
    reset_msg = 'reset password done'
    if Auth.ResetPassword(user_id, old_pwd, new_pwd):
        return render_template('profile.html', user=user, reset_msg=reset_msg)
    else:
        error_pwd = 'the old password does not correct.'
        return render_template('resetpassword.html', error_pwd=error_pwd)
    


@app.route('/sell')
def Sell():
    user_id = session.get('user_id')

    if user_id:
        pass
    else:
        return redirect(url_for('SignIn'))
    
    

@app.route('/items')
def Items():
    category = request.args.get('category')
    return 'hi'







    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
