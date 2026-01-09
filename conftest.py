import pytest 

from main import BooksCollector
from tests import TestBooksCollector

# Фикстура создает новый экземпляр BooksCollector перед каждым тестом
@pytest.fixture(scope="class")
def collector():
    return BooksCollector()


    