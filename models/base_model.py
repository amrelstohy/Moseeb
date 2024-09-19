from datetime import datetime
from uuid import uuid4
import models
import models.engine


class BaseModel():

    def __init__(self, **kwargs):
        format = '%Y-%m-%d %H:%M:%S'
        if not kwargs:
            from models import storage
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
            if self.__class__.__name__ == 'User':
                self.first_name, self.last_name = '', ''
                self.email, self.phone = '', ''
                self.favourites, self.comments, self.items = [], [], []
                self.birthday = ''
                self.gender = ''
                self.img = ''
            if self.__class__.__name__ == 'Item':
                self.user_id = ''
                self.title, self.details = '', ''
                self.price = 0
                self.category = ''
                self.images, self.comments = [], []
                self.category = ''
                self.location_lang, self.location_lat = 0.0, 0.0
            if self.__class__.__name__ == 'Comment':
                self.user_id, self.item_id = '', ''
                self.text = ''

        else:
            del kwargs['__class__']
            for key, value in kwargs.items():
                self.__dict__[key] = value
            self.__dict__['created_at'] = datetime.strptime(self.__dict__['created_at'], format)
            self.__dict__['updated_at'] = datetime.strptime(self.__dict__['updated_at'], format)

    def __str__(self):
        return str(self.__dict__)
    
    def to_dict(self):
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        dictionary['updated_at'] = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        return dictionary
    
    def save(self):
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
        


    
            

   





"""y = BaseModel()
x = BaseModel(**{'name':'amr', 'email':'amr@gmail.com', 'password':'123', 'created_at':'2024-08-31 22:38:11', 'updated_at':'2024-08-31 22:38:11', '__class__':'User'})
print(y.__dict__)
print(x.__dict__)"""

