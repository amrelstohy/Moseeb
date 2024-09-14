from web_flask import app
from models.user import User
from models import storage
from models.auth import Auth

email = 'aaaaaaaaaaaaaaaaaaaaaa@gmail.com'
password = 'aa123'
if Auth.SignUp(email):
    x = User()
    x.email = email
    Auth.save(email, password, x.id)
    x.sell('iphone', 30000, 'pro max', '',)
    x.comment(x.items[0], 'nice')
    x.favourite(x.items[0])

storage.save()