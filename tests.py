from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
 
    # добавляем новую книгу в словарь без указания жанра
    def test_add_new_book_valid_name(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.books_genre
        assert collector.books_genre["Гарри Поттер"] == ""  

    # тест для валидных значений названия книги
    def test_add_new_book_name_too_long(self, collector):
        name = "О" * 40
        collector.add_new_book(name)
        assert name in collector.books_genre
        assert collector.books_genre[name] == ""

    # тест для не валидных значений названия книги
    def test_long_book_name_not_added(self, collector):
        name = "О" * 41
        collector.add_new_book(name)
        assert name not in collector.books_genre

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