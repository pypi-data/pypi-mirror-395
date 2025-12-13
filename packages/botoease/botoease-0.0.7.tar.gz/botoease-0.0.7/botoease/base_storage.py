from abc import ABC, abstractmethod

class BaseStorage(ABC):
    """
    Base interface for all storage backends.
    Every storage provider must implement these methods.
    """

    @abstractmethod
    def upload(self, filepath, filename=None):
        pass

    @abstractmethod
    def delete(self, filename):
        pass

    @abstractmethod
    def generate_url(self, filename, expires=3600):
        pass
