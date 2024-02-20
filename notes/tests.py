from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Note, NoteUpdate

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_signup(self):
        url = reverse('user-signup')
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        url = reverse('user-login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_note_create(self):
        url = reverse('note-create')
        data = {'title': 'Test Note', 'content': 'Test content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_share_note(self):
        note = Note.objects.create(title='Test Note', content='Test content', author=self.user)
        url = reverse('note-share')
        data = {'note_id': note.id, 'user_ids': [self.user.id]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_by_id(self):
        note = Note.objects.create(title='Test Note', content='Test content', author=self.user)
        url = reverse('get_note_by_id', args=[note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Note')

    def test_update_note_by_id(self):
        note = Note.objects.create(title='Test Note', content='Test content', author=self.user)
        url = reverse('update_note_by_id', args=[note.id])
        data = {'content': 'Updated content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_note_version_history(self):
        note = Note.objects.create(title='Test Note', content='Test content', author=self.user)
        url = reverse('note-version-history', args=[note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
