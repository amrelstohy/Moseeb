from flask import Flask, render_template, request, session, url_for, redirect, abort
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
        user.save()
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
        return render_template('sell_form.html')
    else:
        return redirect(url_for('SignIn'))
    
@app.route('/sell/submit', methods=['POST'])
def SellSubmit():
    from models.user import User
    user_id = session.get('user_id')
    title = request.form.get('title')
    category = request.form.get('category')
    price = request.form.get('price')
    details = request.form.get('details')

    if not (title and price and details):
        error_msg = 'please complete all required fields'
        return render_template('sell_form.html', title=title, price=price, details=details, error_msg=error_msg)
    else:
        user = storage.all('User').get(user_id)
        item = user.sell(title, price, category, details)
        return redirect(url_for('Show', id=item.id))
    
@app.route('/items/<string:id>')
def Show(id):
    item = storage.all('Item').get(id)
    if item:
        user = storage.all('User').get(item.user_id)
    else:
        return abort(404)
    if item:
        return render_template('show.html', item=item, user=user)
    
@app.route('/items/<string:id>/edit')
def EditItem(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('SignIn'))
    
    item = storage.all('Item').get(id)
    item_user_id = item.user_id

    if user_id == item_user_id:
        return render_template('sell_edit_form.html', id=id, title=item.title, price=item.price, details=item.details)
    else:
        abort(404)
    
@app.route('/items/<string:id>/edit/submit', methods=['Post'])
def EditItemSubmit(id):
    title = request.form.get('title')
    category = request.form.get('category')
    price = request.form.get('price')
    details = request.form.get('details')

    if not (title and price and details):
        error_msg = 'please complete all required fields'
        return render_template('sell_edit_form.html', id=id, title=title, price=price, details=details, error_msg=error_msg)
    else:
        item = storage.all('Item').get(id)
        item.title = title
        item.category = category
        item.price = price
        item.details = details
        item.save()
        return redirect(url_for('Show', id=item.id))
    


@app.route('/items/<string:id>/delete')
def DeleteItem(id):
    user_id = session.get('user_id')
    if not user_id:
        abort(404)
    
    item = storage.all('Item').get(id)
    item_user_id = item.user_id

    if user_id == item_user_id:
        storage.delete(id, 'Item')
        return redirect(url_for('home'))
    else:
        abort(404)

@app.route('/profile/delete')
def DeleteUser():
    user_id = session.get('user_id')
    if not user_id:
        abort(404)
    
    storage.delete(user_id, 'User')
    session.pop('user_id', None)
    return redirect(url_for('home'))
    





    
    

@app.route('/items')
def Items():
    category = request.args.get('category', 'all')  # Default to 'all' if no category is provided
    page = request.args.get('page', 1, type=int)  # Default to page 1
    items_per_page = 2
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    all_items = list(storage.all('Item').values())
    
    # Filter items by category
    if category == 'phones':
        filtered_items = [item for item in all_items if item.category == 'phones']
    elif category == 'watches':
        filtered_items = [item for item in all_items if item.category == 'watches']
    elif category == 'accessories':
        filtered_items = [item for item in all_items if item.category == 'accessories']
    elif category == 'all':
        filtered_items = all_items
    else:
        abort(404)  # If an invalid category is given, return a 404 page

    # Paginate items
    paginated_items = filtered_items[start:end]
    has_next = len(filtered_items) > end  # Check if there's a next page

    return render_template(
        'items.html', 
        items=paginated_items, 
        page=page, 
        category=category, 
        has_next=has_next
    )






    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
