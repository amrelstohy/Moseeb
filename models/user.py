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
        self.favourites.append(item_id)

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
            storage.new(comment)
            storage.save()
            return True
        except Exception as e:
            print("sjdhjhdvj")

    def sell(self, title, price, details, images, location_lang=0.0, location_lat=0.0):
        from models.item import Item
        from models import storage
        try:
            item = Item()
            item.user_id = self.id
            item.title = title
            item.price = price
            item.details = details
            item.images = images
            item.location_lang = location_lang
            item.location_lat = location_lat
            self.items.append(item.id)
            storage.new(item)
            storage.save()
        except Exception as e:
            print(e)



"""x = User(**{'name': 'amr', 'email': 'amr@gmail.com', 'password': '123', 'created_at': '2024-08-31 22:38:11', 'updated_at': '2024-08-31 22:38:11', '__class__': 'User'})
print(x)
y = User()
print(y.to_dict())"""

        
