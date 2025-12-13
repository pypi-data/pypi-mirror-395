import os
import shutil
from .base_storage import BaseStorage

class LocalStorage(BaseStorage):
    def __init__(self, folder="uploads"):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)

    def upload(self, filepath, filename=None):
        if not filename:
            filename = os.path.basename(filepath)

        dest = os.path.join(self.folder, filename)
        shutil.copy(filepath, dest)

        return {
            "storage": "local",
            "path": dest,
            "filename": filename
        }

    def delete(self, filename):
        path = os.path.join(self.folder, filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        raise FileNotFoundError(f"{filename} not found")

    def generate_url(self, filename, expires=3600):
        return os.path.abspath(os.path.join(self.folder, filename))
