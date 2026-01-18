import pytest
import sys
import os

# Добавляем родительскую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from books_collector import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        return BooksCollector()
    
    @pytest.mark.parametrize("name, expected", [
        ("", False),
        ("А", True),
        ("A", True),
        ("Книга", True),
        ("A" * 40, True),
        ("A" * 41, False),
    ])
    def test_add_new_book_name_length_boundaries(self, collector, name, expected):
        collector.add_new_book(name)
        if expected:
            assert name in collector.books_genre
        else:
            assert name not in collector.books_genre
    
    # Тесты для add_new_book
    def test_add_new_book_valid_name(self, collector):
        collector.add_new_book("Гарри Поттер")
        assert "Гарри Поттер" in collector.books_genre
        assert collector.books_genre["Гарри Поттер"] == ""

    def test_add_new_book_name_already_exists(self, collector):
        collector.add_new_book("1984")
        collector.add_new_book("1984")  # Повторное добавление
        assert len(collector.books_genre) == 1  # Только одна книга

    def test_add_new_book_invalid_name_too_short(self, collector):
        collector.add_new_book("")
        assert "" not in collector.books_genre

    def test_add_new_book_invalid_name_too_long(self, collector):
        long_name = "A" * 41
        collector.add_new_book(long_name)
        assert long_name not in collector.books_genre

    # Тесты для set_book_genre
    def test_set_book_genre_valid(self, collector):
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Фантастика")
        assert collector.books_genre["1984"] == "Фантастика"

    def test_set_book_genre_book_not_in_collection(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.books_genre

    def test_set_book_genre_invalid_genre(self, collector):
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Недопустимый жанр")
        assert collector.books_genre["1984"] == ""  # Жанр не должен измениться

    # Тесты для get_book_genre
    def test_get_book_genre_exists(self, collector):
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Фантастика")
        assert collector.get_book_genre("1984") == "Фантастика"

    def test_get_book_genre_not_exists(self, collector):
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_get_book_genre_no_genre_set(self, collector):
        collector.add_new_book("Книга без жанра")
        assert collector.get_book_genre("Книга без жанра") == ""

    # Тесты для get_books_with_specific_genre
    def test_get_books_with_specific_genre_valid(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.set_book_genre("Книга 2", "Фантастика")
        books = collector.get_books_with_specific_genre("Фантастика")
        assert len(books) == 2
        assert "Книга 1" in books
        assert "Книга 2" in books

    def test_get_books_with_specific_genre_no_books(self, collector):
        books = collector.get_books_with_specific_genre("Фантастика")
        assert books == []

    def test_get_books_with_specific_genre_invalid_genre(self, collector):
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Фантастика")
        books = collector.get_books_with_specific_genre("Недопустимый жанр")
        assert books == []

    def test_get_books_with_specific_genre_mixed_genres(self, collector):
        collector.add_new_book("Фантастическая")
        collector.add_new_book("Ужасная")
        collector.add_new_book("Детективная")
        collector.set_book_genre("Фантастическая", "Фантастика")
        collector.set_book_genre("Ужасная", "Ужасы")
        collector.set_book_genre("Детективная", "Детективы")
        
        fantasy_books = collector.get_books_with_specific_genre("Фантастика")
        assert fantasy_books == ["Фантастическая"]

    # Тесты для get_books_genre
    def test_get_books_genre_empty(self, collector):
        assert collector.get_books_genre() == {}

    def test_get_books_genre_with_books(self, collector):
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Фантастика")
        assert collector.get_books_genre() == {"Книга 1": "Фантастика"}

    # Тесты для get_books_for_children
    def test_get_books_for_children_all_valid(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.set_book_genre("Книга 2", "Комедии")
        books = collector.get_books_for_children()
        assert len(books) == 2
        assert "Книга 1" in books
        assert "Книга 2" in books

    def test_get_books_for_children_exclude_age_rating(self, collector):
        collector.add_new_book("Страшная книга")
        collector.add_new_book("Детектив")
        collector.set_book_genre("Страшная книга", "Ужасы")
        collector.set_book_genre("Детектив", "Детективы")
        books = collector.get_books_for_children()
        assert books == []

    def test_get_books_for_children_mixed_ages(self, collector):
        collector.add_new_book("Фантастика для детей")
        collector.add_new_book("Ужастик")
        collector.add_new_book("Мультфильм")
        collector.set_book_genre("Фантастика для детей", "Фантастика")
        collector.set_book_genre("Ужастик", "Ужасы")
        collector.set_book_genre("Мультфильм", "Мультфильмы")
        
        children_books = collector.get_books_for_children()
        assert len(children_books) == 2
        assert "Фантастика для детей" in children_books
        assert "Мультфильм" in children_books
        assert "Ужастик" not in children_books

    def test_get_books_for_children_no_genre(self, collector):
        collector.add_new_book("Книга без жанра")
        books = collector.get_books_for_children()
        assert books == []

    # Тесты для add_book_in_favorites
    def test_add_book_in_favorites_valid(self, collector):
        collector.add_new_book("1984")
        collector.add_book_in_favorites("1984")
        assert "1984" in collector.favorites

    def test_add_book_in_favorites_already_in_favorites(self, collector):
        collector.add_new_book("1984")
        collector.add_book_in_favorites("1984")
        collector.add_book_in_favorites("1984")  # Повторное добавление
        assert collector.favorites.count("1984") == 1  # Не должно дублироваться

    def test_add_book_in_favorites_book_not_in_collection(self, collector):
        collector.add_book_in_favorites("Несуществующая книга")
        assert "Несуществующая книга" not in collector.favorites

    # Тесты для delete_book_from_favorites
    def test_delete_book_from_favorites_exists(self, collector):
        collector.add_new_book("1984")
        collector.add_book_in_favorites("1984")
        collector.delete_book_from_favorites("1984")
        assert "1984" not in collector.favorites

    def test_delete_book_from_favorites_not_exists(self, collector):
        collector.add_new_book("1984")
        collector.add_book_in_favorites("1984")
        collector.delete_book_from_favorites("Несуществующая книга")
        assert len(collector.favorites) == 1
        assert "1984" in collector.favorites

    # Тесты для get_list_of_favorites_books
    def test_get_list_of_favorites_books_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_with_books(self, collector):
        collector.add_new_book("1984")
        collector.add_new_book("Мастер и Маргарита")
        collector.add_book_in_favorites("1984")
        collector.add_book_in_favorites("Мастер и Маргарита")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert "1984" in favorites
        assert "Мастер и Маргарита" in favorites

    def test_get_list_of_favorites_books_after_deletion(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")
        collector.delete_book_from_favorites("Книга 1")
        
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 1
        assert "Книга 2" in favorites
        assert "Книга 1" not in favorites

    # Интеграционные тесты
    def test_integration_full_flow(self, collector):
        # Добавляем книги
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        
        # Устанавливаем жанры
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.set_book_genre("Книга 2", "Ужасы")
        
        # Добавляем в избранное
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")
        
        # Проверяем
        assert collector.get_book_genre("Книга 1") == "Фантастика"
        assert collector.get_books_with_specific_genre("Ужасы") == ["Книга 2"]
        assert collector.get_books_for_children() == ["Книга 1"]
        assert set(collector.get_list_of_favorites_books()) == {"Книга 1", "Книга 2"}
        
        # Удаляем из избранного
        collector.delete_book_from_favorites("Книга 2")
        assert collector.get_list_of_favorites_books() == ["Книга 1"]

    def test_add_multiple_books_same_favorites(self, collector):
        collector.add_new_book("Книга A")
        collector.add_new_book("Книга B")
        collector.add_new_book("Книга C")
        
        collector.add_book_in_favorites("Книга A")
        collector.add_book_in_favorites("Книга B")
        collector.add_book_in_favorites("Книга C")
        
        assert len(collector.get_list_of_favorites_books()) == 3
        
        collector.delete_book_from_favorites("Книга B")
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert "Книга A" in favorites
        assert "Книга C" in favorites
        assert "Книга B" not in favorites

    def test_books_genre_independent_from_favorites(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.add_book_in_favorites("Книга 1")
        
        # Удаление из избранного не должно влиять на жанр
        collector.delete_book_from_favorites("Книга 1")
        assert collector.get_book_genre("Книга 1") == "Фантастика"
        assert "Книга 1" in collector.books_genre