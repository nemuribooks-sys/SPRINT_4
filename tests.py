import pytest 

from test_data import SYMBOL

@pytest.mark.usefixtures("collector")
class TestBooksCollector:
    
    def test_add_new_book_valid_name(self, collector):
        collector.add_new_book('1984')
        assert '1984' in collector.books_genre
        assert collector.books_genre['1984'] == ''

    # Параметризованный тест для проверки граничных значений длины названия
    @pytest.mark.parametrize("name, expected", SYMBOL)
    def test_add_new_book_name_length_boundaries(collector, name, expected):
       collector.add_new_book(name)
       assert (name in collector.books_genre) == expected

    # проверяем, что одну и ту же книгу можно добавить только один раз
    def test_add_new_book_duplicate(self, collector):
        collector.add_new_book("Книга")
        collector.add_new_book("Книга")
        assert len(collector.books_genre) == 1

    # проверяем, что метод добавляет только входящие в список жанры книг
    def test_set_book_genre_book_not_exists(self, collector):
        collector.set_book_genre("Неправильная", "Фантастика")
        assert "Неправильная" not in collector.books_genre

    # проверяем, что метод добавляет только входящие в словарь книги
    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Неправильный жанр")
        assert collector.books_genre["Гарри Поттер"] == ""

    # проверяем, что метод определяет жанр книги по ее названию
    def test_get_book_genre_exists(self, collector):
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Комедии")
        assert collector.get_book_genre("Книга") == "Комедии"

    # проверяем, что метод не находит несуществующих книг в списке 
    def test_get_book_genre_not_exists(self, collector):
        assert collector.get_book_genre("Неправильная") is None

    # проверяем, что в списке жанров находятся все ожидаемые жанры
    def test_genre_list_contains_all_expected_genres(self, collector):
        expected_genres = ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        for genre in expected_genres:
            assert genre in collector.genre, f"Жанр '{genre}' должен быть в списке genre"

    # проверяем, что метод находит книги определенного жанра
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.set_book_genre("Книга2", "Фантастика")
        
        result = collector.get_books_with_specific_genre("Фантастика")
        assert len(result) == 2
        assert "Книга1" in result
        assert "Книга2" in result

    # проверяем, что метод выводит текущий словарь
    def test_get_books_genre(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        assert collector.get_books_genre() == {"Книга1": "", "Книга2": ""}

    # проверяем, что метод показывает книги только для детей
    def test_get_books_for_children(self, collector):
        collector.add_new_book("Детская книга")
        collector.add_new_book("Взрослая книга")
        collector.set_book_genre("Детская книга", "Мультфильмы")
        collector.set_book_genre("Взрослая книга", "Ужасы")
        result = collector.get_books_for_children()
        assert result == ["Детская книга"]

    # проверяем, что метод не добавляет книги без жанра в списке книг для детей
    def test_get_books_for_children_no_genre(self, collector):
        collector.add_new_book("Книга без жанра")
        result = collector.get_books_for_children()
        assert result == []

    # проверяем, что метод добавляет книги с правильным названием в избранное 
    def test_add_book_in_favorites_valid(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        assert "Книга" in collector.favorites

    def test_add_book_in_favorites_book_not_in_genre(self, collector):
        collector.add_book_in_favorites("Неправильная")
        assert "Неправильная" not in collector.favorites

    # проверяем, что метод повторно не добавляет книгу в избранное 
    def test_add_book_in_favorites_duplicate(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.add_book_in_favorites("Книга")
        assert collector.favorites.count("Книга") == 1

    # проверяем, что метод удаляет книгу из избранного
    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book("Книга")
        collector.add_book_in_favorites("Книга")
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.favorites

    # проверяем, что метод показывает список избранных книг
    def test_get_list_of_favorites_books(self, collector):
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert "Книга1" in favorites
        assert "Книга2" in favorites