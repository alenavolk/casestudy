from django.test import TestCase
from rest_framework.test import APIRequestFactory

from src.books.models import Country, Language, Book
from src.books.views import BookViewSet


class BookTestCase(TestCase):
    fixtures = ['fixtures/countries.json', 'fixtures/languages.json', 'fixtures/books.json']

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_returns_all_books(self):
        self.request = self.factory.get('/books/')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 76)
        self.assertEqual(response.data[0]['title'], "Things Fall Apart")

    def test_returns_books_in_correct_order(self):
        self.request = self.factory.get('/books/?order_by=title')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.data[0]['title'], "A Doll's House")
        self.assertEqual(response.data[-1]['title'], "Zorba the Greek")

        self.request = self.factory.get('/books/?order_by=year')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.data[0]['title'], "The Epic Of Gilgamesh")
        self.assertEqual(response.data[0]['year'], -1700)

        self.request = self.factory.get('/books/?order_by=-year')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.data[0]['title'], "Beloved")
        self.assertEqual(response.data[0]['year'], 1987)

    def test_returns_books_in_default_order_if_field_error(self):
        self.request = self.factory.get('/books/?order_by=qwerty')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], "Things Fall Apart")

    def test_filters_books_by_country(self):
        self.request = self.factory.get('/books/?country=United States')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data[0]['title'], "Invisible Man")
        country_id = response.data[0]['country']
        self.assertEqual(Country.objects.get(id=country_id).name, "United States")

    def test_returns_nothing_if_incorrect_country_value(self):
        self.request = self.factory.get('/books/?country=querty')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(len(response.data), 0)

    def test_filters_books_by_language(self):
        self.request = self.factory.get('/books/?language=German')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(len(response.data), 7)
        self.assertEqual(response.data[0]['title'], "Faust")
        language_id = response.data[0]['language']
        self.assertEqual(Language.objects.get(id=language_id).name, "German")

    def test_returns_nothing_if_incorrect_language_value(self):
        self.request = self.factory.get('/books/?language=querty')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(len(response.data), 0)

    def test_filters_books_by_country_and_language(self):
        self.request = self.factory.get('/books/?country=Ireland&language=English')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Gulliver's Travels")
        country_id = response.data[0]['country']
        self.assertEqual(Country.objects.get(id=country_id).name, "Ireland")
        language_id = response.data[0]['language']
        self.assertEqual(Language.objects.get(id=language_id).name, "English")

    def test_filters_books_by_country_and_language_and_returns_in_correct_order(self):
        self.request = self.factory.get('/books/?country=Russia&language=Russian&order_by=-pages')
        response = BookViewSet.as_view({'get': 'list'})(self.request)
        self.assertEqual(len(response.data), 9)
        self.assertEqual(response.data[0]['title'], "War and Peace")
        country_id = response.data[0]['country']
        self.assertEqual(Country.objects.get(id=country_id).name, "Russia")
        language_id = response.data[0]['language']
        self.assertEqual(Language.objects.get(id=language_id).name, "Russian")
        self.assertEqual(response.data[0]['pages'], 1296)

    def test_returns_one_book(self):
        request = self.factory.get('/books/24/')
        response = BookViewSet.as_view({'get': 'retrieve'})(request, pk=24)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], "Madame Bovary")
        self.assertEqual(Book.objects.get(id=24).title, "Madame Bovary")
