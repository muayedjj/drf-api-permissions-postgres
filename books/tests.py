from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Book


class BookTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        testuser2 = get_user_model().objects.create_user(
            username="testuser2", password="pass"
        )
        testuser1.save()

        test_book = Book.objects.create(
            title="treasure_island",
            owner=testuser1,
            synopsis="Fifteen dead men for a wooden chest",
        )
        test_book.save()

    def setUp(self):
        self.client.login(username='testuser1', password="pass")

    def test_books_model(self):
        book = Book.objects.get(id=1)
        actual_owner = str(book.owner)
        actual_title = str(book.title)
        actual_summary = str(book.synopsis)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_title, "treasure_island")
        self.assertEqual(
            actual_summary, "Fifteen dead men for a wooden chest"
        )

    def test_get_book_list(self):
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        books = response.data
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "treasure_island")

    def test_auth_required(self):
        self.client.logout()
        url = reverse("book_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_can_delete(self):
        self.client.logout()
        self.client.login(username='testuser2', password="pass")
        url = reverse("book_detail", args=[1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
