from rest_framework import serializers

from documents.models import Document, DocumentCategory, DocumentType

class DocumentTypeSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DocumentCategory.objects.filter(is_deleted=False),
        source='category',
        write_only=True
    )
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DocumentType
        fields = [
            'id',
            'category_id',
            'category',
            'title',
            'private_visible',
            'public_visible',
            'is_active',
            'is_deleted',
        ]
        read_only_fields = ['id', 'is_deleted']

    def validate(self, attrs):
        # -------------------------------------
        return attrs

class DocumentCategorySerializer(serializers.ModelSerializer):
    types = DocumentTypeSerializer(many=True, write_only=True)

    class Meta:
        model = DocumentCategory
        fields = ['id', 'company', 'participant', 'title', 'is_deleted', 'types']
        read_only_fields = ['id', 'is_deleted']

    def create(self, validated_data):
        types_data = validated_data.pop('types', [])
        category = DocumentCategory.objects.create(**validated_data)
        for type_data in types_data:
            DocumentType.objects.create(category=category, **type_data)
        return category



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