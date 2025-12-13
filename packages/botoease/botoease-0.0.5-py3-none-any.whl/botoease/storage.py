from .s3_handler import S3Handler
from .local_handler import LocalHandler

class Storage:
    def __init__(self, backend: str = "local", **kwargs):
        """
        backend: "local" or "s3"
        kwargs: backend-specific settings
        """

        self.backend = backend.lower()

        if self.backend == "s3":
            self.handler = S3Handler(
                bucket=kwargs.get("bucket"),
                region=kwargs.get("region"),
                access_key=kwargs.get("access_key"),
                secret_key=kwargs.get("secret_key")
            )
        elif self.backend == "local":
            self.handler = LocalHandler(
                folder=kwargs.get("folder", "uploads")
            )
        else:
            raise ValueError(f"Invalid storage type: {self.backend}")   

    def upload(self, filepath, filename=None):
        return self.handler.upload(filepath, filename)

    def delete(self, filename):
        return self.handler.delete(filename)

    def generate_url(self, filename, expires=3600):
        return self.handler.generate_url(filename, expires)   