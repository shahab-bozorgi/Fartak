from documents.models import Document
from documents.tasks import extract_and_save_pdf_text, delete_uploaded_text

class DocumentService:
    @staticmethod
    def ensure_single_active(document_type):
        old_active = Document.objects.filter(
            document_type=document_type,
            is_active=True,
            is_deleted=False
        ).first()

        if old_active:
            old_active.is_active = False
            old_active.save()

            if document_type.public_visible or document_type.private_visible:
                delete_uploaded_text.delay(old_active.id)

    @staticmethod
    def save_uploaded_text(document):
        extract_and_save_pdf_text.delay(document.id)

    @staticmethod
    def soft_delete(document):
        document.is_deleted = True
        document.save()
