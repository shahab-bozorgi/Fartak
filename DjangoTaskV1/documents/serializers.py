from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from documents.models import Document, DocumentCategory, DocumentType
from documents.services.category import DocumentCategoryService

class DocumentRequestId(serializers.Serializer):
    id = serializers.IntegerField()

class DocumentTypeSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentCategory.objects.filter(is_deleted=False),
        source='category',
        write_only=True
    )
    category = serializers.StringRelatedField(read_only=True)
    document_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DocumentType
        fields = [
            'id',
            'category_id',
            'category',
            'title',
            'private_visible',
            'public_visible',
            'document_count',
            'is_active',
            'is_deleted',
        ]
        read_only_fields = ['id', 'is_deleted']

class GetDocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ['id', 'company', 'participant', 'title', 'is_deleted']

class DocumentCategorySerializer(serializers.ModelSerializer):
    types = DocumentTypeSerializer(many=True, write_only=True)
    document_types = DocumentTypeSerializer(source='types', many=True, read_only=True)

    class Meta:
        model = DocumentCategory
        fields = ['id', 'company', 'participant', 'title', 'is_deleted', 'types', 'document_types']
        read_only_fields = ['id', 'is_deleted']

    def create(self, validated_data):
        return DocumentCategoryService.create_category_with_types(validated_data)

    def update(self, instance, validated_data):
        return DocumentCategoryService.update_category_with_types(instance, validated_data)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id',
            'company',
            'participant',
            'document_type',
            'file',
            'is_active',
            'is_deleted',
        ]
        read_only_fields = ['id', 'is_deleted']

    def validate(self, attrs):
        doc_type = attrs.get("document_type")

        if doc_type:
            has_active = Document.objects.filter(
                document_type=doc_type,
                is_active=True,
                is_deleted=False
            ).exists()

            if not has_active:
                attrs["is_active"] = True
            else:
                attrs["is_active"] = attrs.get("is_active", False)

        return attrs


class DocumentTypeWithCountSerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField()

    class Meta:
        model = DocumentType
        fields = [
            'id',
            'title',
            'is_active',
            'public_visible',
            'private_visible',
            'document_count',
        ]


class CategoryWithDocTypeStatsSerializer(serializers.ModelSerializer):
    types = serializers.SerializerMethodField()

    class Meta:
        model = DocumentCategory
        fields = [
            'id',
            'title',
            'participant',
            'company',
            'types',
        ]

    def get_types(self, obj):
        types = getattr(obj, 'documenttype_set', [])
        return DocumentTypeWithCountSerializer(types, many=True).data