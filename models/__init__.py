from models.engine import file_storage
from models.auth import Auth
storage = file_storage.FileStorage()
storage.reload()
Auth.reload()