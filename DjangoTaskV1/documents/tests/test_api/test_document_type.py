from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from documents.models import Document, DocumentType, Participant, DocumentCategory


class DocumentTypeAPITestCase(APITestCase):
    def setUp(self):
        self.participant = Participant.objects.create(
            first_name="Alice", last_name="Smith", status="active"
        )
        self.category = DocumentCategory.objects.create(
            company=1,
            participant=self.participant,
            title="Category for Type"
        )
        self.type = DocumentType.objects.create(
            category=self.category,
            title="Existing Type",
            private_visible=True,
            public_visible=False,
            is_active=True,
            is_deleted=False
        )
        self.type_data = {
            "category_id": self.category.id,
            "title": "New Type",
            "private_visible": False,
            "public_visible": True,
            "is_active": True
        }

    def test_list_document_types(self):
        url = reverse('document-type-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d['id'] == self.type.id for d in response.data['results']))

    def test_create_document_type_with_valid_category(self):
        url = reverse('document-type-list-create')
        response = self.client.post(url, self.type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.type_data['title'])

    def test_create_document_type_with_invalid_category(self):
        url = reverse('document-type-list-create')
        invalid_data = self.type_data.copy()
        invalid_data['category_id'] = 9999  # nonexistent
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category_id', response.data)

    def test_retrieve_document_type(self):
        url = reverse('document-type-detail', kwargs={'pk': self.type.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.type.title)

    def test_update_document_type(self):
        url = reverse('document-type-detail', kwargs={'pk': self.type.id})
        update_data = {
            "category_id": self.category.id,
            "title": "Updated Type",
            "private_visible": False,
            "public_visible": True,
            "is_active": False
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Type")

    def test_partial_update_document_type(self):
        url = reverse('document-type-detail', kwargs={'pk': self.type.id})
        response = self.client.patch(url, {"title": "Partial Updated"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Partial Updated")

    def test_soft_delete_document_type(self):
        url = reverse('document-type-detail', kwargs={'pk': self.type.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.type.refresh_from_db()
        self.assertTrue(self.type.is_deleted)