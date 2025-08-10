from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from documents.models import Participant, DocumentCategory, DocumentType

class DocumentCategoryAPITestCase(APITestCase):
    def setUp(self):
        self.participant = Participant.objects.create(
            first_name="John", last_name="Doe", status="active"
        )
        self.category_data = {
            "company": 1,
            "participant": self.participant.id,
            "title": "Test Category",
            "types": [
                {"title": "Type 1", "private_visible": True, "public_visible": False, "is_active": True}
            ]
        }
        self.category = DocumentCategory.objects.create(
            company=1,
            participant=self.participant,
            title="Existing Category"
        )
        self.type = DocumentType.objects.create(
            category=self.category,
            title="Existing Type",
            private_visible=True,
            public_visible=True,
            is_active=True,
            is_deleted=False
        )

    def test_list_categories(self):
        url = reverse('document-category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

    def test_create_category_with_types(self):
        url = reverse('document-category-list-create')
        response = self.client.post(url, self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.category_data['title'])
        self.assertEqual(len(response.data['types']), 1)

    def test_retrieve_category(self):
        url = reverse('document-category-detail', kwargs={'pk': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.category.title)

    def test_update_category(self):
        url = reverse('document-category-detail', kwargs={'pk': self.category.id})
        new_data = {
            "company": 2,
            "participant": self.participant.id,
            "title": "Updated Title",
            "types": [
                {
                    "id": self.type.id,
                    "title": "Updated Type",
                    "private_visible": False,
                    "public_visible": True,
                    "is_active": False
                }
            ]
        }
        response = self.client.put(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")
        self.assertEqual(response.data['types'][0]['title'], "Updated Type")

    def test_partial_update_category(self):
        url = reverse('document-category-detail', kwargs={'pk': self.category.id})
        response = self.client.patch(url, {"title": "Partial Update"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Partial Update")

    def test_soft_delete_category(self):
        url = reverse('document-category-detail', kwargs={'pk': self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.category.refresh_from_db()
        self.assertTrue(self.category.is_deleted)
