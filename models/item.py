from models.base_model import BaseModel

class Item(BaseModel):
    """user_id = ''
    title = ''
    details = ''
    price = 0
    images = []
    comments = []
    location_lang = 0.0
    location_lat = 0.0"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)