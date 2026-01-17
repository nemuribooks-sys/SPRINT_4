import pytest 

from bookscollector import BooksCollector

# Фикстура создает новый экземпляр BooksCollector перед каждым тестом
@pytest.fixture(scope="class")
def collector():
    return BooksCollector()


    