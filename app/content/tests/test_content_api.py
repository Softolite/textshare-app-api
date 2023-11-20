"""
Tests for Text Content APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Content

from content.serializers import (
    ContentSerializer,
    ContentDetailSerializer,
)


CONTENTS_URL = reverse('content:content-list')


def detail_url(content_id):
    """Create and return a content detail URL."""
    return reverse('content:content-detail', args=[content_id])


def create_content(user, **params):
    """Create and return a sample content."""
    defaults = {
        'title': 'Sample content title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/content.pdf',
    }
    defaults.update(params)

    content = Content.objects.create(user=user, **defaults)
    return content


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicContentAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CONTENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContentApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_contents(self):
        """Test retrieving a list of contents."""
        create_content(user=self.user)
        create_content(user=self.user)

        res = self.client.get(CONTENTS_URL)

        contents = Content.objects.all().order_by('-id')
        serializer = ContentSerializer(contents, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_content_list_limited_to_user(self):
        """Test list of contents is limited to authenticated user."""
        other_user = create_user(email='other@example.com', password='test123')
        create_content(user=other_user)
        create_content(user=self.user)

        res = self.client.get(CONTENTS_URL)

        contents = Content.objects.filter(user=self.user)
        serializer = ContentSerializer(contents, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_content_detail(self):
        """Test get content detail."""
        content = create_content(user=self.user)

        url = detail_url(content.id)
        res = self.client.get(url)

        serializer = ContentDetailSerializer(content)
        self.assertEqual(res.data, serializer.data)

    def test_create_content(self):
        """Test creating a content."""
        payload = {
            'title': 'Sample content',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        res = self.client.post(CONTENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        content = Content.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(content, k), v)
        self.assertEqual(content.user, self.user)

    def test_partial_update(self):
        """Test partial update of a content."""
        original_link = 'https://example.com/content.pdf'
        content = create_content(
            user=self.user,
            title='Sample content title',
            link=original_link,
        )

        payload = {'title': 'New content title'}
        url = detail_url(content.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        content.refresh_from_db()
        self.assertEqual(content.title, payload['title'])
        self.assertEqual(content.link, original_link)
        self.assertEqual(content.user, self.user)

    def test_full_update(self):
        """Test full update of content."""
        content = create_content(
            user=self.user,
            title='Sample content title',
            link='https://exmaple.com/content.pdf',
            description='Sample content description.',
        )

        payload = {
            'title': 'New content title',
            'link': 'https://example.com/new-content.pdf',
            'description': 'New content description',
            'time_minutes': 10,
            'price': Decimal('2.50'),
        }
        url = detail_url(content.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        content.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(content, k), v)
        self.assertEqual(content.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the content user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        content = create_content(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(content.id)
        self.client.patch(url, payload)

        content.refresh_from_db()
        self.assertEqual(content.user, self.user)

    def test_delete_content(self):
        """Test deleting a content successful."""
        content = create_content(user=self.user)

        url = detail_url(content.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Content.objects.filter(id=content.id).exists())

    def test_content_other_users_content_error(self):
        """Test trying to delete another users content gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        content = create_content(user=new_user)

        url = detail_url(content.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Content.objects.filter(id=content.id).exists())