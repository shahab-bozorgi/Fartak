from celery import shared_task
from PyPDF2 import PdfReader
from documents.models import UploadedTextFile, Document

@shared_task
def extract_and_save_pdf_text(document_id):
    try:
        document = Document.objects.get(id=document_id)
        file = document.file
        doc_type = document.document_type

        if (
            document.is_active and
            (doc_type.public_visible or doc_type.private_visible) and
            file.name.endswith(".pdf")
        ):
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            UploadedTextFile.objects.create(
                document=document,
                document_type=doc_type,
                text=text
            )
    except Exception as e:
        print(f"[Celery] PDF extract error: {e}")


@shared_task
def delete_uploaded_text(document_id):
    UploadedTextFile.objects.filter(document_id=document_id).delete()
