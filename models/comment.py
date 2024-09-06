from models.base_model import BaseModel

class Comment(BaseModel):
    """user_id = ''
    text = ''
    item_id = ''"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)