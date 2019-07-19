from abc import ABC, abstractmethod
from faker import Faker


class DataTemplate(ABC):

    def __init__(self, format="delimited", delimiter=","):
        self.faker = Faker()
        self.format = format
        self.delimiter = delimiter
        super().__init__()

    @abstractmethod
    def generate(self):
        pass
