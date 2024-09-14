import json
import bcrypt
from models.user import User

class Auth():
    __file = 'users.json'
    __users = {}

    def __init__(self):
        pass

    @classmethod
    def SignUp(cls, email):
        if email in cls.__users:
            print('this email is used before')
            return
        return True

    @classmethod
    def SignIn(cls, email, password):
        if email not in cls.__users:
            return 'email'
        if bcrypt.checkpw(password.encode('utf-8'), cls.__users[email]['password'].encode('utf-8')):
            return cls.__users[email]['user_id']
        return 'password'
    @classmethod
    def save(cls, email, password, user_id):
        salt = bcrypt.gensalt()
        cls.__users[email] = {'password':bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8'), 'user_id':user_id}
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


            
            