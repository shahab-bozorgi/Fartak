from django.db.models import Count, Q, Prefetch

from documents.models import DocumentCategory, DocumentType


class DocumentCategoryService:
    @staticmethod
    def create_category_with_types(validated_data):
        types_data = validated_data.pop('types', [])
        category = DocumentCategory.objects.create(**validated_data)
        for type_data in types_data:
            type_data.pop('category', None)
            DocumentType.objects.create(category=category, **type_data)
        return category

    @staticmethod
    def update_category_with_types(instance, validated_data):
        types_data = validated_data.pop('types', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if types_data is not None:
            sent_type_ids = [t.get('id') for t in types_data if t.get('id') is not None]
    
            instance.types.exclude(id__in=sent_type_ids).delete()

            for type_data in types_data:
                type_id = type_data.pop('id', None)
                type_data.pop('category', None)

                if type_id:
                    try:
                        doc_type = instance.types.get(id=type_id)
                        for attr, value in type_data.items():
                            setattr(doc_type, attr, value)
                        doc_type.save()
                    except DocumentType.DoesNotExist:
                        continue
                else:
                    DocumentType.objects.create(category=instance, **type_data)

        return instance

    @staticmethod
    def soft_delete_category(instance):
        instance.is_deleted = True
        instance.save()



class CategoryService:
    @staticmethod
    def get_filtered_categories_with_types(participant_id=None, category_id=None, has_active_type=None):
        queryset = DocumentCategory.objects.filter(is_deleted=False)

        if participant_id:
            queryset = queryset.filter(participant_id=participant_id)

        if category_id:
            queryset = queryset.filter(id=category_id)

        if has_active_type == 'true':
            queryset = queryset.filter(
                types__is_active=True,
                types__is_deleted=False
            ).distinct()

        annotated_types = DocumentType.objects.filter(is_deleted=False).annotate(
            document_count=Count('document', filter=Q(document__is_deleted=False))
        )

        return queryset.prefetch_related(
            Prefetch('types', queryset=annotated_types)
        )
