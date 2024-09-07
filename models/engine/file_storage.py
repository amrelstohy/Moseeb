from models.base_model import BaseModel
from models.user import User
from models.comment import Comment
from models.item import Item
import json

class FileStorage():
    __data = {'users':{}, 'items':{}, 'comments':{}}
    __file = 'data.json'



  
    classes = {'User':User, 'Comment':Comment, 'Item':Item}

    @classmethod
    def all(cls, classname):
        if classname == 'User':
            return cls.__data['users']
        elif classname == 'Item':
            return cls.__data['items']
        elif classname == 'Comment':
            return cls.__data['comments']
        
    def new(self, obj):
        cls = obj.__class__.__name__
        if cls == 'User':
            self.__data['users'].update({obj.id:obj})
            return self.__data['users'][obj.id]
        elif cls == 'Item':
            self.__data['items'].update({obj.id:obj})
            return self.__data['items'][obj.id]
        elif cls == 'Comment':
            self.__data['comments'].update({obj.id:obj})
            return self.__data['comments'][obj.id]
        
    @classmethod
    def save(cls):
        try:
            with open(cls.__file, 'w') as f:
                temp = {'users':{}, 'items':{}, 'comments':{}}
                for key, value in cls.__data['users'].items():
                    temp['users'][key] = value.to_dict()
                for key, value in cls.__data['items'].items():
                    temp['items'][key] = value.to_dict()
                for key, value in cls.__data['comments'].items():
                    temp['comments'][key] = value.to_dict()
                json.dump(temp, f)

        except Exception as e:
            print(e)

    @classmethod
    def reload(cls):
        try:
            with open(cls.__file, 'r') as f:
                temp = json.load(f)
                for key, value in temp['users'].items():
                    cls.__data['users'][key] = User(**value)
                
                for key, value in temp['items'].items():
                    cls.__data['items'][key] = Item(**value)

                for key, value in temp['comments'].items():
                    cls.__data['comments'][key] = Comment(**value)
        except Exception as e:
            print(e)

    @classmethod
    def delete(cls, id, classname):
        classes = ['User', 'Item', 'Comment']
        if classname not in classes:
            return False
        if classname == 'User':
            try:
                user = cls.__data['users'][id]
                for comment in user.comments:
                    item_id = cls.__data['comments'][comment].item_id
                    del cls.__data['comments'][comment]
                    cls.__data['items'][item_id].comments.remove(comment)
                for item in user.items:
                    for comment in cls.__data['items'][item].comments:
                        user_id = cls.__data['comments'][comment].user_id
                        cls.__data['users'][user_id].comments.remove(comment)
                        del cls.__data['comments'][comment]
                    del cls.__data['items'][item]
                del cls.__data['users'][id]
            except Exception as e:
                print(e)

        if classname == 'Item':
            try:
                item = cls.__data['items'][id]
                user_id = item.user_id
                for comment in item.comments:
                    user_id = cls.__data['comments'][comment].user_id
                    cls.__data['users'][user_id].comments.remove(comment)
                    del cls.__data['comments'][comment]
                
                del cls.__data['items'][id]
                cls.__data['users'][user_id].items.remove(id)
            except Exception as e:
                print(e)

        if classname == 'Comment':
            try:
                user_id = cls.__data['comments'][id].user_id
                item_id = cls.__data['comments'][id].item_id
                cls.__data['users'][user_id].comments.remove(id)
                cls.__data['items'][item_id].comments.remove(id)
                del cls.__data['comments'][id]
            except Exception as e:
                print(e)




