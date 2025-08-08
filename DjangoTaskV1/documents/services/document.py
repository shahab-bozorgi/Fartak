from PyPDF2 import PdfReader
from documents.models import Document, UploadedTextFile


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
                UploadedTextFile.objects.filter(document=old_active).delete()

    @staticmethod
    def extract_pdf_text(file):
        try:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            print(f"PDF reading error: {e}")
            return ""

    @staticmethod
    def save_uploaded_text(document):
        file = document.file
        doc_type = document.document_type

        if (
            document.is_active and
            (doc_type.public_visible or doc_type.private_visible) and
            file.name.endswith(".pdf")
        ):
            text = DocumentService.extract_pdf_text(file)
            UploadedTextFile.objects.create(
                document=document,
                document_type=doc_type,
                text=text
            )

    @staticmethod
    def soft_delete(document):
        document.is_deleted = True
        document.save()
