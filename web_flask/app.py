from flask import Flask, render_template, request, session, url_for, redirect, abort
from models import *
from models import storage
from flask_wtf import CSRFProtect
import secrets
from models.auth import Auth
from werkzeug.utils import secure_filename
import os
import shutil



app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 
csrf = CSRFProtect(app)

UPLOAD_FOLDER = 'web_flask/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif', 'heif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
        password_error = 'Wrong password'
        return render_template('signin/form.html', email=email, password=password, password_error=password_error )
    else:
        session['user_id'] = auth.get('user_id')
        session['superuser'] = auth.get('superuser')
        next_url = request.args.get('next')

    return redirect(next_url or url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('superuser', None)
    return redirect(url_for('home'))


@app.route('/profile')
def MyProfile():
    user = storage.all('User').get(session.get('user_id'))
    if user:
        items = []
        for item_id in user.items:
            item = storage.all('Item').get(item_id)
            if item:
                items.append(item)
        return render_template('myprofile.html', user=user, items=items)
    else:
        return redirect(url_for('SignIn', next=request.url))
    
@app.route('/profile/<string:id>')
def Profile(id):
    user = storage.all('User').get(id)
    if not user:
        abort(404)
    items = []
    for item_id in user.items:
        item = storage.all('Item').get(item_id)
        if item:
            items.append(item)
    return render_template('profile.html', user=user, items=items)

@app.route('/profile/<string:id>/delete')
def DeleteUser(id):
    superuser = session.get('superuser')
    user = storage.all('User').get(id)
    if not user:
        abort(404)

    if superuser:
        storage.delete(id, 'User')
        return redirect(url_for('home'))
    else:
        abort(404)

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
    
    user_id = Auth.SignUp(fname, lname, email, phone, pwd, False, gender)
    if not user_id:
        error_msg = 'this email exists before.'
        return render_template('signup/form.html', fname=fname, lname=lname,
                            email=email, phone=phone, error_msg=error_msg)
    
    user = storage.all('User').get(user_id)

    profile_image = request.files['profile_image']
    if profile_image and allowed_file(profile_image.filename):
        filename = secure_filename(profile_image.filename)
        file_ext = os.path.splitext(filename)[1]
        new_filename = f"{user_id}{file_ext}"
        profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_images/' + new_filename))

    else:
        new_filename = ''

    user.img = new_filename
    storage.save()
    
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
    user_id = session.get('user_id')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    profile_image = request.files['profile_image']

    if profile_image and allowed_file(profile_image.filename):
        filename = secure_filename(profile_image.filename)
        file_ext = os.path.splitext(filename)[1]
        new_filename = f"{user_id}{file_ext}"
        profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], 'profile_images/' + new_filename))
    else:
        new_filename = None

    if not (fname and lname and phone):
        error_msg = 'please complete all required fields'
        return render_template('update.html', fname=fname, lname=lname, phone=phone, error_msg=error_msg)
    else:
        
        user = storage.all('User').get(user_id)
        """if user.img:
            old_path = os.path.join(app.config['UPLOAD_FOLDER'],'profile_images/' + user.img)
            if os.path.exists(old_path):
                os.remove(old_path)"""
        user.first_name = fname
        user.last_name = lname
        user.phone = phone
        if new_filename:
            user.img = new_filename
        user.save()
        return redirect(url_for('MyProfile'))
    
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
    user_id = session.get('user_id')
    title = request.form.get('title')
    category = request.form.get('category')
    price = request.form.get('price')
    details = request.form.get('details')

    if not (title and price and details) and 'images' not in request.files or not request.files.getlist('images'):
        error_msg = 'please complete all required fields'
        return render_template('sell_form.html', title=title, price=price, details=details, error_msg=error_msg)
    else:
        user = storage.all('User').get(user_id)
        item = user.sell(title, price, category, details)
        images = request.files.getlist('images')
        
        path = app.config['UPLOAD_FOLDER'] + f'items_images/{item.id}/'
        if not os.path.exists(path):
            os.makedirs(path)
        for image in images:
            if image.filename == '':
                continue

            original_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'items_images/{item.id}/' + original_filename))
            item.images.append(original_filename)
            storage.save()
        return redirect(url_for('Show', id=item.id))

@app.route('/items/<string:id>')
def Show(id):
    item = storage.all('Item').get(id)
    if item:
        user = storage.all('User').get(item.user_id)
    else:
        return abort(404)
    if item:
        comments = []
        users = []
        for comment_id in item.comments:
            comment = storage.all('Comment').get(comment_id)
            user = storage.all('User').get(comment.user_id)
            if comment and user:
                comments.append(comment)
                users.append(user)
        return render_template('show.html', item=item, user=user, comments=comments, users=users)
 
@app.route('/items/<string:id>/comment')
def Comment(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('SignIn', next=request.url))
    comment = request.form.get('comment')
    user = storage.all('User').get(user_id)
    user.comment(id, comment)
    return redirect(url_for('Show', id=id))

@app.route('/items/<string:item_id>/deletecomment')
def DeleteComment(item_id):
    comment_id = request.args.get('comment_id')
    item = storage.all('Item').get(item_id)
    if comment_id not in item.comments:
        return redirect(url_for('Show', id=item_id))
    
    user = session.get('user_id')
    superuser = session.get('superuser')
    if not user:
        return redirect(url_for('SignIn', next=request.url))
    
    if (user == item.user_id) or superuser:
        storage.delete(comment_id, 'Comment')
        return redirect(url_for('Show', id=item_id))
    
    abort(404)


@app.route('/items/<string:id>/favourite')
def Favourite(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('SignIn', next=request.url))
    user = storage.all('User').get(user_id)
    user.favourite(id)
    return redirect(url_for('Show', id=id))

@app.route('/items/<string:id>/unfavourite')
def UnFavourite(id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('SignIn', next=request.url))
    user = storage.all('User').get(user_id)
    user.unfavourite(id)
    return redirect(url_for('Show', id=id))


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
    item = storage.all('Item').get(id)

    if not (title and price and details):
        error_msg = 'please complete all required fields'
        return render_template('sell_edit_form.html', id=id, title=title, price=price, details=details, error_msg=error_msg)
    else:
        
        if 'images' in request.files or  request.files.getlist('images'):
            images = request.files.getlist('images')
        
            path = app.config['UPLOAD_FOLDER'] + f'items_images/{id}/'
            if os.path.exists(path):
                shutil.rmtree(path)
                os.makedirs(path)
                item.images = []
            else:
                os.makedirs(path)
                item.images = []
            for image in images:
                if image.filename == '':
                    continue
                original_filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], f'items_images/{item.id}/' + original_filename))
                item.images.append(original_filename)

        item.title = title
        item.category = category
        item.price = price
        item.details = details
        item.save()
        return redirect(url_for('Show', id=item.id))
    


@app.route('/items/<string:id>/delete')
def DeleteItem(id):
    user_id = session.get('user_id')
    superuser = session.get('superuser')
    if not user_id:
        abort(404)
    
    item = storage.all('Item').get(id)
    item_user_id = item.user_id

    if (user_id == item_user_id) or superuser:
        storage.delete(id, 'Item')
        return redirect(url_for('home'))
    else:
        abort(404)

@app.route('/profile/delete')
def DeleteProfile():
    user_id = session.get('user_id')
    if not user_id:
        abort(404)
    
    storage.delete(user_id, 'User')
    session.pop('user_id', None)
    return redirect(url_for('home'))
    

@app.route('/items')
def Items():
    category = request.args.get('category', 'all') 
    page = request.args.get('page', 1, type=int) 
    items_per_page = 2
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    all_items = list(storage.all('Item').values())
    
    if category == 'phones':
        filtered_items = [item for item in all_items if item.category == 'phones']
    elif category == 'watches':
        filtered_items = [item for item in all_items if item.category == 'watches']
    elif category == 'accessories':
        filtered_items = [item for item in all_items if item.category == 'accessories']
    elif category == 'all':
        filtered_items = all_items
    else:
        abort(404)

    paginated_items = filtered_items[start:end]
    has_next = len(filtered_items) > end

    return render_template(
        'items.html', 
        items=paginated_items, 
        page=page, 
        category=category, 
        has_next=has_next
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
