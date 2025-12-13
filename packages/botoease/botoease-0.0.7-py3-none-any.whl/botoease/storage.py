from .local_storage import LocalStorage
from .s3_storage import S3Storage

class Storage:
    """
    Factory class that returns the correct backend implementation.
    This is the public-facing API.
    """

    def __init__(self, backend="local", **kwargs):
        backend = backend.lower()

        if backend == "local":
            self.impl = LocalStorage(folder=kwargs.get("folder", "uploads"))

        elif backend == "s3":
            self.impl = S3Storage(
                bucket=kwargs.get("bucket"),
                region=kwargs.get("region"),
                access_key=kwargs.get("access_key"),
                secret_key=kwargs.get("secret_key"),
            )

        else:
            raise ValueError("Invalid backend. Use 'local' or 's3'.")

    def upload(self, filepath, filename=None):
        return self.impl.upload(filepath, filename)

    def delete(self, filename):
        return self.impl.delete(filename)

    def generate_url(self, filename, expires=3600):
        return self.impl.generate_url(filename, expires)
