import os
import shutil
from datetime import datetime


class LocalHandler:
    def __init__(self, folder="uploads"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def upload(self, filepath, filename=None):
        if filename is None:
            filename = os.path.basename(filepath)
        destination = os.path.join(self.folder, filename)
        shutil.copy2(filepath, destination)
        return {
            "storage": "local",
            "path": destination,
            "filename": filename
        }

    def delete(self, filename):
        filepath = os.path.join(self.folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def generate_url(self, filename, expires=3600):
        # local storage -> file path only
        return os.path.abspath(os.path.join(self.folder, filename))
