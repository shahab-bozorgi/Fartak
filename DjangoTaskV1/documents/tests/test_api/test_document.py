from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from documents.models import Document, DocumentType, Participant, DocumentCategory

class DocumentAPITestCase(APITestCase):
    def setUp(self):
        self.participant = Participant.objects.create(
            first_name="Bob", last_name="Brown", status="active"
        )
        self.category = DocumentCategory.objects.create(
            company=1,
            participant=self.participant,
            title="Doc Category"
        )
        self.type = DocumentType.objects.create(
            category=self.category,
            title="Doc Type",
            private_visible=True,
            public_visible=True,
            is_active=True,
            is_deleted=False
        )
        self.document = Document.objects.create(
            company=1,
            participant=self.participant,
            document_type=self.type,
            file='files/documents/testfile.pdf',
            is_active=True,
            is_deleted=False
        )
        self.document_data = {
            "company": 1,
            "participant": self.participant.id,
            "document_type": self.type.id,
            "file": None,  # فایل در تست با SimpleUploadedFile ارسال می‌شود
            "is_active": True
        }

    def test_list_documents(self):
        url = reverse('document-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d['id'] == self.document.id for d in response.data['results']))

    def test_create_document(self):
        url = reverse('document-list-create')
        test_file = SimpleUploadedFile("test.pdf", b"file_content", content_type="application/pdf")
        data = self.document_data.copy()
        data['file'] = test_file
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['participant'], self.participant.id)

    def test_retrieve_document(self):
        url = reverse('document-detail', kwargs={'pk': self.document.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.document.id)

    def test_update_document(self):
        url = reverse('document-detail', kwargs={'pk': self.document.id})
        update_data = {
            "company": 2,
            "participant": self.participant.id,
            "document_type": self.type.id,
            "is_active": False
        }
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(self.document.company, 2)
        self.assertFalse(self.document.is_active)

    def test_soft_delete_document(self):
        url = reverse('document-detail', kwargs={'pk': self.document.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.document.refresh_from_db()
        self.assertTrue(self.document.is_deleted)