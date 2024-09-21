import json
import bcrypt
from models.user import User


class Auth():
    __file = 'users.json'
    __users = {}

    def __init__(self):
        pass

    @classmethod
    def SignUp(cls,fname, lname, email, phone, pwd, superuser=False, gender=None, img=None):
        from models import storage
        if email in cls.__users:
            print('this email is used before')
            return
        user = User()
        user.first_name = fname
        user.last_name = lname
        user.email = email
        user.phone = phone
        user.gender = gender
        user.img = img
        storage.save()
        cls.save(email, pwd, user.id, superuser)
        return user.id

    @classmethod
    def SignIn(cls, email, password):
        if email not in cls.__users:
            return 'email'
        if bcrypt.checkpw(password.encode('utf-8'), cls.__users[email]['password'].encode('utf-8')):
            return {'user_id':cls.__users[email]['user_id'], 'superuser':cls.__users[email].get('superuser')}
        return 'password'
    
    @classmethod
    def ResetPassword(cls, user_id, old_pwd, new_pwd):
        from models import storage
        email = storage.all('User').get(user_id).email

        if bcrypt.checkpw(old_pwd.encode('utf-8'), cls.__users[email]['password'].encode('utf-8')):
            cls.save(email, new_pwd, user_id)
            return True
        

    @classmethod
    def save(cls, email, password, user_id, suberuser=False):
        salt = bcrypt.gensalt()
        cls.__users[email] = {'password':bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'), 'user_id':user_id, 'superuser':suberuser}
        try:
            with open(cls.__file, 'w') as file:
                json.dump(cls.__users, file)
        except Exception as e:
            print(e)

    @classmethod
    def reload(cls):
        try:
            with open(cls.__file, 'r') as file:
                cls.__users = json.load(file)
        except Exception as e:
            print(e)


            
            