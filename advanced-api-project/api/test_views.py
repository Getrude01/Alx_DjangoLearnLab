from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        # Create authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='J.R.R. Tolkien')

        # Create books
        self.book1 = Book.objects.create(title='Harry Potter', publication_year=1997, author=self.author1)
        self.book2 = Book.objects.create(title='The Hobbit', publication_year=1937, author=self.author2)

        # API client
        self.client = APIClient()

    # -----------------------------
    # Test: List Books
    # -----------------------------
    def test_list_books(self):
        url = reverse('book_list')  # Ensure this matches your urls.py name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -----------------------------
    # Test: Retrieve Book
    # -----------------------------
    def test_retrieve_book(self):
        url = reverse('book_detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Harry Potter')

    # -----------------------------
    # Test: Create Book (authenticated)
    # -----------------------------
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book_create')
        data = {
            'title': 'Fantastic Beasts',
            'publication_year': 2001,
            'author': self.author1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, 'Fantastic Beasts')

    # -----------------------------
    # Test: Create Book (unauthenticated)
    # -----------------------------
    def test_create_book_unauthenticated(self):
        url = reverse('book_create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -----------------------------
    # Test: Update Book
    # -----------------------------
    def test_update_book(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book_update', kwargs={'pk': self.book1.id})
        data = {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'publication_year': 1997,
            'author': self.author1.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter and the Philosopher\'s Stone')

    # -----------------------------
    # Test: Delete Book (admin only)
    # -----------------------------
    def test_delete_book_admin(self):
        self.client.login(username='admin', password='admin123')
        url = reverse('book_delete', kwargs={'pk': self.book2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_delete_book_non_admin(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('book_delete', kwargs={'pk': self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------------
    # Test: Filtering
    # -----------------------------
    def test_filter_books_by_author(self):
        url = reverse('book_list') + f'?author={self.author1.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)

    # -----------------------------
    # Test: Search
    # -----------------------------
    def test_search_books(self):
        url = reverse('book_list') + '?search=Hobbit'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    # -----------------------------
    # Test: Ordering
    # -----------------------------
    def test_order_books_by_publication_year_desc(self):
        url = reverse('book_list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)
