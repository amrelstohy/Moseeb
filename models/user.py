from models.base_model import BaseModel
from datetime import datetime

class User(BaseModel):
    """eamil = ''
    password = ''
    first_name = ''
    last_name = ''
    phone = ''
    items = []
    favourites = []
    comments = []
    birthday = datetime
    gender = ''"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def favourite(self, item_id):
        from models import storage
        if item_id in self.favourites:
            return
        self.favourites.append(item_id)
        storage.save()

    def unfavourite(self, item_id):
        from models import storage
        if item_id in self.favourites:
            self.favourites.remove(item_id)
            storage.save()
        

    def comment(self, item_id, text):
        from models.comment import Comment
        from models import storage
        try:
            comment = Comment()
            comment.user_id = self.id
            comment.item_id = item_id
            comment.text = text
            self.comments.append(comment.id)
            storage.all('Item')[item_id].comments.append(comment.id)
            storage.save()
            return True
        except Exception as e:
            print("sjdhjhdvj")

    def sell(self, title, price, category, details, location_lang=0.0, location_lat=0.0):
        from models.item import Item
        from models import storage
        try:
            item = Item()
            item.user_id = self.id
            item.title = title
            item.price = price
            item.category = category
            item.details = details
            item.location_lang = location_lang
            item.location_lat = location_lat
            item.images = []
            self.items.append(item.id)
            storage.save()
            return item
        except Exception as e:
            print(e)



"""x = User(**{'name': 'amr', 'email': 'amr@gmail.com', 'password': '123', 'created_at': '2024-08-31 22:38:11', 'updated_at': '2024-08-31 22:38:11', '__class__': 'User'})
print(x)
y = User()
print(y.to_dict())"""

        
