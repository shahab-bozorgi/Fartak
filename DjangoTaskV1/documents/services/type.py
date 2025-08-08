from documents.models import DocumentType, UploadedTextFile


class DocumentTypeService:
    @staticmethod
    def validate_category_exists(category_id):
        from documents.models import DocumentCategory
        return DocumentCategory.objects.filter(id=category_id, is_deleted=False).exists()

    @staticmethod
    def soft_delete(document_type: DocumentType):
        document_type.is_deleted = True
        document_type.save()

    @staticmethod
    def cleanup_uploaded_text_if_visibility_removed(old_instance: DocumentType, new_instance: DocumentType):
        visibility_changed = (
            old_instance.is_active != new_instance.is_active or
            old_instance.private_visible != new_instance.private_visible or
            old_instance.public_visible != new_instance.public_visible
        )

        should_cleanup = not (
            new_instance.is_active and
            (new_instance.private_visible or new_instance.public_visible)
        )

        if visibility_changed and should_cleanup:
            UploadedTextFile.objects.filter(document_type=new_instance).delete()