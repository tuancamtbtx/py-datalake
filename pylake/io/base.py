from abc import ABC, abstractmethod

class BaseIO(ABC):
    def __init__(self,verbose):
        self.verbose = verbose

    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def get_client(self):
        pass